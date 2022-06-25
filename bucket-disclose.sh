#!/bin/bash

# Using error messages to decloak an S3 bucket. Uses soap, unicode, post, multipart, 
# streaming and index listing as ways of figure it out. You do need a valid aws-key 
# (never the secret) to properly get the error messages

#### FORKED FROM https://gist.github.com/bl4de/35d5831e6eb4a29fe40626efbea7818e
#### Written by Frans Rosén (twitter.com/fransrosen)


_debug="$2" #turn on debug
_timeout="20"
#you need a valid key, since the errors happens after it validates that the key exist. we do not need the secret key, only access key
_aws_key=$AWS_KEY

H_ACCEPT="accept-language: en-US,en;q=0.9,sv;q=0.8,zh-TW;q=0.7,zh;q=0.6,fi;q=0.5,it;q=0.4,de;q=0.3"
H_AGENT="user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36"

_log_file="./bucket-disclose.log"
_sed_bin=$(which gsed)
if [ "${_sed_bin}" == "" ]; then
  _sed_bin=$(which sed)
fi

_timeout_bin=$(which gtimeout)
if [ "${_timeout_bin}" == "" ]; then
  _timeout_bin=$(which timeout)
fi

r=$(echo "$1" | ${_sed_bin} -E 's/^[a-z]+:\/\///') #raw but without protocol
d=$(echo "$r" | cut -d "/" -f 1) #domain
pr=$(echo "$1" | ${_sed_bin} -E 's/(^[a-z]+:\/\/)?.*/\1/') #protocol, could be empty, use http if so
if [ "$pr" == "" ]; then pr="http://"; fi
pd="${pr}${d}" #protocol and domain always and only
u=$(echo "$1") #full url
p="${pr}$(echo "${r}" | rev | cut -d "/" -f 2- | rev)" # path without trailing slash (will be weird when bucket is in dir, but will be found later on)

result() {
	echo "$1" >> $_log_file
	[ "$1" != "" ] && echo "$1" && exit 0;
}

debug() {
	echo "* $1" >> $_log_file
	[ "$_debug" != "" ] && echo "* $1"
}

is_bucket_already() {
	_no_protocol=$(echo "$1" | ${_sed_bin} -E 's/^[a-z]+:\/\///') # function is reused after, make sure we clean up proto
	_comp=$(echo "${_no_protocol}" | grep -vE "^[^:]*s3[^:]+amazonaws.*") #check if domain contains s3.*amazonaws.com
	if [ "${_comp}" == "" ]; then
		result $(echo "${_no_protocol}" | grep -E '^s3.*amazon[^/]+\/.*' | cut -d "/" -f 2)
		result $(echo "${_no_protocol}" | grep -E '^[^:]+.s3.*amazon.*' | ${_sed_bin} -E 's/^([^\:]+).s3[^:]+amazon.*$/\1/');
	fi
}

is_bucket() {
	debug "checking if bucket: ${1}..."
	_response=$(${_timeout_bin} ${_timeout} curl -H "${H_ACCEPT}" -H "${H_AGENT}" "${1}" -sL -D- --insecure --max-time 5 | \
		grep -iE "^x-amz-error-code|^server: amazons3|<Code>AccessDenied</Code>|Code: AccessDenied|NoSuchKey")
}

is_bucket_soap() {
	debug "checking if bucket using soap... ${1}/soap"
	_response=$(${_timeout_bin} ${_timeout} curl -H "${H_ACCEPT}" -H "${H_AGENT}" "${1}/soap" -X POST -sL -D- --insecure --max-time 5 | \
		grep ">Missing SOAPAction header<")
}

is_bucket_invalid_char() {
	debug "checking if bucket using invalid char: ${1}/%83..."
	_response=$(${_timeout_bin} ${_timeout} curl -H "${H_ACCEPT}" -H "${H_AGENT}" "${1}/%83" -sL -D- --insecure --max-time 5 | \
		grep -iE "<Code>InvalidURI</Code>|Code: InvalidURI|NoSuchKey")
}

is_bucket_invalid_method() {
	debug "checking if bucket using invalid method... ${1}/xyz"
	_response=$(${_timeout_bin} ${_timeout} curl -H "${H_ACCEPT}" -H "${H_AGENT}" "${1}/xyz" -X POSTX -sL -D- --insecure --max-time 5 | \
		grep "<Code>BadRequest</Code><Message>")
	if [ "${_response}" != "" ]; then
		_response="${1}/xyz"
	else
		_response=""
	fi
}

is_bucket_listable() {
	debug "checking if bucket is listable... ${1}/?abc"
	_response=$(${_timeout_bin} ${_timeout} curl -H "${H_ACCEPT}" -H "${H_AGENT}" -sL "${1}/?abc" --insecure --max-time 5 | \
		grep "<ListBucketResult" -A 1 | grep -Eo "<Name>[^<]+</Name>" | cut -d ">" -f 2 | cut -d "<" -f 1)
}

is_bucket_domain() {
	debug "checking if domain exists as bucket: http://${1}.s3.amazonaws.com..."
	_response=$(${_timeout_bin} ${_timeout} curl -H "${H_ACCEPT}" -H "${H_AGENT}" "http://${1}.s3.amazonaws.com" -sL --insecure --max-time 5 | grep -E "ListBucketResult|AccessDenied|PermanentRedirect") 
}

is_bucket_redirectable() {
	debug "checking if url redirects to bucket... ${1}/xyzadad"
	_response=$(${_timeout_bin} ${_timeout} curl -H "${H_ACCEPT}" -H "${H_AGENT}" -sL "$1/xyzadad" -D- | grep -i "^location:" | grep amazonaws | cut -d " " -f 2)
	_response=$(is_bucket_already "${_response}") #remove s3-domain stuff
}

is_redirecting() {
	debug "check if URL redirects to other domain... ${1}"
	_response=$(curl -Ls -o /dev/null -H "${H_ACCEPT}" -H "${H_AGENT}" -w %{url_effective} "${1}")
	_od=$(echo "${1}" | ${_sed_bin} -E 's/^[a-z]+:\/\///' | cut -d "/" -f 1)
	_rd=$(echo "${_response}" | ${_sed_bin} -E 's/^[a-z]+:\/\///' | cut -d "/" -f 1)
	if [ "${_od}" == "${_rd}" ]; then
		_response=""
	fi
}

bucket_unicode_sign_error() {
	debug "checking unicode-error... ${1}/åäö"
	_response=$(${_timeout_bin} ${_timeout} curl -H "${H_ACCEPT}" -H "${H_AGENT}" -sL "${1}/åäö" --insecure --max-time 5 | grep "host:" | grep "amazonaws.com" | cut -d ":" -f 2)
	_response=$(is_bucket_already "${_response}") #remove s3-domain stuff
}

bucket_post_sign_error() {
	debug "checking post-error... ${1}/okok?456"
	_response=$(${_timeout_bin} ${_timeout} curl -H "${H_ACCEPT}" -H "${H_AGENT}" "${1}/okok?456" -H "Authorization: AWS ${_aws_key}:x" -H \
		"Date: $(date -u +%a,\ %d\ %b\ %Y\ %H:%M:%S\ GMT)" -sL | \
		grep "</StringToSign>" | \
		cut -d "<" -f 1 | cut -d "/" -f 2)
}

bucket_get_sign_error() {
	debug "checking get-error... ${1}/okok?AWSAccessKey..."
	_response=$(${_timeout_bin} ${_timeout} curl -X GET -H "${H_ACCEPT}" -H "${H_AGENT}" "${1}/okok?AWSAccessKeyId=${_aws_key}&Expires=$(expr $(date +%s) + 1000)&Signature=x" -H \
		"Date: $(date -u +%a,\ %d\ %b\ %Y\ %H:%M:%S\ GMT)" -sL | \
		grep "</StringToSign>" | \
		cut -d "<" -f 1 | cut -d "/" -f 2)
}

bucket_put_sign_error() {
	debug "checking put-error... ${1}/okok?AWSAccessKey..."
	_response=$(${_timeout_bin} ${_timeout} curl -X PUT -H "${H_ACCEPT}" -H "${H_AGENT}" "${1}/okok?AWSAccessKeyId=${_aws_key}&Expires=$(expr $(date +%s) + 1000)&Signature=x" -H \
		"Date: $(date -u +%a,\ %d\ %b\ %Y\ %H:%M:%S\ GMT)" -sL | \
		grep "</StringToSign>" | \
		cut -d "<" -f 1 | cut -d "/" -f 2)
}

bucket_multipart_sign_error() {
	debug "checking multipart-error... ${1}/?789"
	_response=$(${_timeout_bin} ${_timeout} curl -H "${H_ACCEPT}" -H "${H_AGENT}" --form "d=x" -X POST "${1}/?789" \
		-H "Authorization: AWS ${_aws_key}:x" -H \
		"Date: $(date -u +%a,\ %d\ %b\ %Y\ %H:%M:%S\ GMT)" -sL | \
		grep "</StringToSign>" | cut -d "<" -f 1 | cut -d "/" -f 2)
}

bucket_streaming_sign_error() {
	debug "checking streaming sign-error... ${1}/ioioio?987"
	_response=$(${_timeout_bin} ${_timeout} curl -H "${H_ACCEPT}" -H "${H_AGENT}" "${1}/ioio?987" -sL -H \
		"Authorization: AWS4-HMAC-SHA256 Credential=${_aws_key}/20180101/ap-south-1/s3/aws4_request,SignedHeaders=date;host;x-amz-acl;x-amz-content-sha256;x-amz-date,Signature=x" -H \
		"Date: $(date -u +%a,\ %d\ %b\ %Y\ %H:%M:%S\ GMT)" -H \
		"x-amz-content-sha256: STREAMING-AWS4-HMAC-SHA256-PAYLOAD" | grep "<CanonicalRequest>" -A 1 | tail -n 1 | cut -d "/" -f 2)
}

change_bucket_location() {
	debug "changing location of bucket... ${1}"
	p="$1"
	_response="1"
}

> $_log_file
debug "start checking... ${u}"
is_bucket_already "${r}"
is_bucket "${pd}"
[ "${_response}" == "" ] && is_bucket_soap "${pd}"
_is_root_bucket="${_response}"
_bucket_location=""

if [ "${_is_root_bucket}" != "" ]; then
	_bucket_location="${pd}"
else
	is_bucket_soap "${p}"
	[ "${_response}" == "" ] && is_bucket "${p}"
	[ "${_response}" == "" ] && is_bucket "${p}/xyzabc" && change_bucket_location "${p}/xyzabc"
	[ "${_response}" == "" ] && is_bucket_invalid_method "${p}"
	[ "${_response}" == "" ] && is_bucket_invalid_char "${p}"

	if [ "${_response}" != "" ]; then
		_bucket_location="${p}"
	fi
fi

if [ "${_bucket_location}" != "" ]; then
	debug "bucket-location: ${_bucket_location}"
	bucket_unicode_sign_error "${_bucket_location}"
	result "${_response}"
	bucket_streaming_sign_error "${_bucket_location}"
	result "${_response}"
	bucket_get_sign_error "${_bucket_location}"
	result "${_response}"
	bucket_post_sign_error "${_bucket_location}"
	result "${_response}"
	bucket_put_sign_error "${_bucket_location}"
	result "${_response}"
	bucket_multipart_sign_error "${_bucket_location}" #this one can bug out with fastly, since host is being different when POST
	result "${_response}"
	is_bucket_listable "${_bucket_location}"
	result "${_response}"
	is_bucket_redirectable "${_bucket_location}"
	result "${_response}"
fi

#if [ "${_is_root_bucket}" ]; then
is_bucket_domain "${d}"
[ "${_response}" != "" ] && result "${d}"
#fi

is_redirecting "${pr}${r}"
[ "${_response}" != "" ] && bash $0 "${_response}" "$2" || debug "location is not a bucket: ${pr}${r} (${_bucket_location})" && exit 1

exit 0
