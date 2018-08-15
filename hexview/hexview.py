#!/usr/bin/python
"""
based on: "Tutorial: Making your own Hex Dump Program" by DrapsTV
https://www.youtube.com/watch?v=B8nRrw_M_nk&index=1&list=WL

"""
import argparse
import os
import itertools
import binascii

ASCII = 'ascii'
CTRL = 'ctrl'
OTHER = 'other'

# https://en.wikipedia.org/wiki/List_of_file_signatures
FILE_SIGNATURES = {
    'a1b2c3d4': 'Libpcap File Format',
    'd4c3b2a1': 'Libpcap File Format',
    '0a0d0d0a': 'PCAP Next Generation Dump File Format (pcapng)',
    'edabeedb': 'RedHat Package Manager (RPM) package',
    '53503031': 'Amazon Kindle Update Package',
    '00': 'IBM Storyboard bitmap file; Windows Program Information File; Mac Stuffit Self-Extracting Archive; IRIS OCR data file',
    'BEBAFECA': 'Palm Desktop Calendar Archive',
    '00014244': 'Palm Desktop To Do Archive',
    '00014454': 'Palm Desktop Calendar Archive',
    '00010000': 'Palm Desktop Data File (Access format)',
    '00000100': 'Computer icon encoded in ICO file format',
    '667479703367': '3rd Generation Partnership Project 3GPP and 3GPP2 multimedia files',
    '1FA0': 'Compressed file (often tar zip) using LZH algorithm',
    '425A68': 'Compressed file using Bzip2 algorithm',
    '474946383761': 'Image file encoded in the Graphics Interchange Format (GIF) - GIF87a',
    '474946383961': 'Image file encoded in the Graphics Interchange Format (GIF) - GIF89a',
    'FFD8FFE00010': 'JPEG raw or in the JFIF or Exif file format',
    '49492A00': 'Tagged Image File Format (tiff, Little Endian format)',
    '4D4D002A': 'Tagged Image File Format (tiff, Big Endian)',
    '49492A0010000000': 'Canon RAW Format Version 2',
    '4352': 'Canon RAW format is based on the TIFF file format',
    '802A5FD7': 'Kodak Cineon image',
    '524E4301': 'Compressed file using Rob Northen Compression version 1',
    '524E4302': 'Compressed file using Rob Northen Compression version 2',
    '53445058': 'SMPTE DPX image (big endian format)',
    '58504453': 'SMPTE DPX image (little endian format)',
    '762F3101': 'OpenEXR image',
    '425047FB': 'Better Portable Graphics',
    'FFD8FFDB': 'JPEG raw or in the JFIF or Exif file format',
    'FFD8FFE000104A4649460001': 'JPEG raw or in the JFIF or Exif file format',
    'FFD8FFE1': 'JPEG raw or in the JFIF or Exif file format',
    '464F52': 'IFF Interleaved Bitmap Image',
    '4C424D': 'IFF Interleaved Bitmap Image',
    '464F52': 'IFF 8-Bit Sampled Voice',
    '535658': 'IFF 8-Bit Sampled Voice',
    '464F524D': 'IFF (misc filetypes)',
    '4C5A4950': 'lzip compressed file',
    '4D5A': 'DOS MZ executable file format and its descendants (including NE and PE)',
    '504B0304': 'zip file format and formats based on it, such as JAR, ODF, OOXML',
    '504B0506': 'zip file format and formats based on it, such as JAR, ODF, OOXML (empty archive)',
    '504B0708': 'zip file format and formats based on it, such as JAR, ODF, OOXML (spanned archive)',
    '526172211A0700': 'RAR archive version 1.50 onwards',
    '526172211A070100': 'RAR archive version 5.0 onwards',
    '7F454C46': 'ELF Executable and Linkable Format',
    '89504E470D0A1A0A': 'Image encoded in the Portable Network Graphics format (PNG)',
    'CAFEBABE': 'Java class file, Mach-O Fat Binary',
    'EFBBBF': 'UTF-8 encoded Unicode byte order mark, commonly seen in text files',
    'FEEDFACE': 'Mach-O binary (32-bit)',
    'FEEDFACF': 'Mach-O binary (64-bit)',
    'CEFAEDFE': 'Mach-O binary (reverse byte ordering scheme, 32-bit)',
    'CFFAEDFE': 'Mach-O binary (reverse byte ordering scheme, 64-bit)',
    'FFFE': 'Byte-order mark for text file encoded in little-endian 16-bit Unicode Transfer Format',
    'FFFE0000': 'Byte-order mark for text file encoded in little-endian 32-bit Unicode Transfer Format',
    '25215053': 'PostScript document',
    '25504446': 'PDF document',
    '3026B2758E66CF11': 'Advanced Systems Format (asf, wma, wmv)',
    'A6D900AA0062CE6C': 'Advanced Systems Format (asf, wma, wmv)',
    '2453444930303031': 'System Deployment Image, a disk image format used by Microsoft',
    '4F676753': 'Ogg, an open source media container format',
    '38425053': 'Photoshop Document file, Adobe Photoshop native file format',
    'FFFB': 'MPEG-1 Layer 3 file without an ID3 tag or with an ID3v1 tag (whichs appended at the end of the file)',
    '494433': 'MP3 file with an ID3v2 container',
    '424D': 'BMP file, a bitmap format used mostly in the Windows world',
    '4344303031': 'ISO9660 CD/DVD image file',
    '53494D504C452020': 'Flexible Image Transport System (FITS)',
    '664C6143': 'Free Lossless Audio Codec (flac)',
    '4D546864': 'MIDI sound file',
    'D0CF11E0A1B11AE1': 'Compound File Binary Format, a container format used for document by older versions of Microsoft Office',
    '6465780A30333500': 'Dalvik Executable',
    '4B444D': 'VMDK files',
    '43723234': 'Google Chrome extension or packaged app',
    '41474433': 'FreeHand 8 document',
    '05070000424F424F': 'AppleWorks 5 document',
    '0607E100424F424F': 'AppleWorks 6 document',
    '455202000000': 'Roxio Toast disc image file, also some .dmg-files begin with same bytes',
    '8B455202000000': 'Roxio Toast disc image file, also some .dmg-files begin with same bytes',
    '7801730D626260': 'Apple Disk Image file',
    '78617221': 'eXtensible ARchive format',
    '504D4F43434D4F43': 'Windows Files And Settings Transfer Repository',
    '4E45531A': 'Nintendo Entertainment System ROM file',
    '7573746172003030': 'tar archive',
    '7573746172202000': 'tar archive',
    '746F7833': 'Open source portable voxel file',
    '4D4C5649': 'Magic Lantern Video file',
    '44434D0150413330': 'Windows Update Binary Delta Compression',
    '377ABCAF271C': '7-Zip File Format',
    '1F8B': 'GZIP file',
    'FD377A585A0000': 'XZ compression utility using LZMA/LZMA2 compression',
    '04224D18': 'LZ4 Frame Format',
    '4D534346': 'Microsoft Cabinet file',
    '535A444488F02733': 'Microsoft compressed file in Quantum format',
    '464C4946': 'Free Lossless Image Format',
    '1A45DFA3': 'Matroska media container, including WebM',
    '3082': 'DER encoded X.509 certificate',
    '4449434D': 'DICOM Medical File Format',
    '774F4646': 'WOFF File Format 1.0',
    '774F4632': 'WOFF File Format 2.0',
    '3c3f786d6c20': 'eXtensible Markup Language (xml) when using the ASCII character encoding',
    '0061736d': 'WebAssembly binary format',
    'cf8401': 'Lepton compressed JPEG image',
    '435753': 'flash .swf',
    '465753': 'flash .swf',
    '213C617263683E': 'linux deb file',
    '52494646': 'Google WebP image file',
    '27051956': 'U-Boot / uImage. Das U-Boot Universal Boot Loader',
    '7B5C72746631': 'Rich Text Format',
    '54415045': 'Microsoft Tape Format',
    '47': 'MPEG Transport Stream (MPEG-2 Part 1)',
    '000001BA': 'MPEG Program Stream (MPEG-1 Part 1 (essentially identical) and MPEG-2 Part 1)',
    '000001B3': 'MPEG Program Stream; MPEG Transport Stream; MPEG-1 video and MPEG-2 video (MPEG-1 Part 2 and MPEG-2 Part 2)',
    '7801': 'zlib (No Compression/low)',
    '789c': 'zlib (Default Compression)',
    '78da': 'zlib (Best Compression)',
    '1F8B0800': 'Minecraft Level Data File (NBT)',
    '62767832': 'LZFSE - Lempel-Ziv style data compression algorithm using Finite State Entropy coding. (bvx2)',
    '4F5243': 'Apache ORC (Optimized Row Columnar) file format',
    '4F626A01': 'Apache Avro binary file format',
    '53455136': 'RCFile columnar file format',
    '65877856': 'PhotoCap Object Templates',
    '5555aaaa': 'PhotoCap Vector',
    '785634': 'PhotoCap Template',
    '50415231': 'Apache Parquet columnar file format',
    '454D5832': 'Emulator Emaxsynth samples',
    '454D5533': 'Emulator III synth samples',
    '1B4C7561': 'Lua bytecode'
}

COLORS = {
    "black": '\33[0;30m\33[40m',
    "white": '\33[0;37m\33[40m',
    "red": '\33[0;31m\33[40m',
    "green": '\33[0;32m\33[40m',
    "green_bg": '\33[1;32m\33[41m',
    "yellow": '\33[0;33m\33[40m',
    "yellow_bg": '\33[1;33m\33[41m',
    "blue": '\33[0;34m\33[40m',
    "magenta": '\33[0;35m\33[40m',
    "magenta_bg": '\33[1;35m\33[41m',
    "cyan": '\33[0;36m\33[40m',
    "grey": '\33[0;90m\33[40m',
    "lightgrey": '\33[0;37m\33[40m',
    "lightblue": '\33[0;94m\33[40m'
}


def file_type(file_signature):
    """
    Recognize file type based on file 'magic numbers'
    """
    file_signature = binascii.hexlify(file_signature).upper()
    recognized = 'ASCII text (no file signature found)'
    for signature in FILE_SIGNATURES:
        if file_signature.startswith(signature.upper()):
            recognized = FILE_SIGNATURES[signature]

    return "{}\n[+] File type: {}{}{}".format(COLORS['cyan'], COLORS['yellow'], recognized, COLORS['white'])


def char_type(c):
    """
    Returns char type depends on its ASCII code
    """
    if 32 < ord(c) < 128:
        return ASCII
    if ord(c) <= 16:
        return CTRL
    return OTHER


def make_color(c, df_c=False):
    """
    Formats color for byte depends on if it's printable ASCII
    """

    # for file diff - if characters are different, use bg color for char:
    diff = (c != df_c) if df_c != False else False
    # printable ASCII:
    if char_type(c) == ASCII:
        if diff:
            retval = "{}{:02X}{}".format(
                COLORS['green_bg'], ord(c), COLORS['white'])
        else:
            retval = "{}{:02X}{}".format(
                COLORS['green'], ord(c), COLORS['white'])
    if char_type(c) == OTHER:
        if diff:
            retval = "{}{:02X}{}".format(
                COLORS['yellow_bg'], ord(c), COLORS['white'])
        else:
            retval = "{}{:02X}{}".format(
                COLORS['yellow'], ord(c), COLORS['white'])
    if char_type(c) == CTRL:
        if diff:
            retval = "{}{:02X}{}".format(
                COLORS['magenta_bg'], ord(c), COLORS['white'])
        else:
            retval = "{}{:02X}{}".format(
                COLORS['magenta'], ord(c), COLORS['white'])

    return retval


def format_text(c):
    """
    Formats color for character depends on if it's printable ASCII
    """
    if char_type(c) == ASCII:
        retval = "{}{}{}".format(COLORS['lightblue'], c, COLORS['white'])
    if char_type(c) == CTRL:
        retval = "{}.{}".format(COLORS['magenta'], COLORS['white'])
    if char_type(c) == OTHER:
        retval = "{}.{}".format(COLORS['yellow'], COLORS['white'])
    return retval


def format_chunk(chunk, start, stop, df_chunk=False, dec=False):
    """
    Formats one full chunk (byte)
    """
    if dec:
        if df_chunk:
            return " ".join("{}:{}{:#04}{} ".format(make_color(c, df_c), COLORS['grey'],
                                                    ord(c), COLORS['white']) for c, df_c in itertools.izip(chunk[start:stop], df_chunk[start:stop]))
        return " ".join("{}:{}{:#04}{} ".format(make_color(c), COLORS['grey'],
                                                ord(c), COLORS['white']) for c in chunk[start:stop])
    else:
        if df_chunk:
            return " ".join("{} ".format(make_color(c, df_c))
                            for c, df_c in itertools.izip(chunk[start:stop], df_chunk[start:stop]))
        return " ".join("{} ".format(make_color(c)) for c in chunk[start:stop])


def extract_shellcode(start, end, read_binary):
    """
    Extract shellcode in hex format, eg. for C exploits, from given range of bytes
    """
    read_binary.seek(start)
    shellcode = ""
    s = read_binary.read(end - start)
    for c in s:
        if ord(c) == 0:
            shellcode = shellcode + "{}".format(COLORS['red']) + str(
                hex(ord(c))).replace("0x", "\\x") + "{}".format(COLORS['white'])
        else:
            shellcode = shellcode + "{}".format(COLORS['yellow']) + str(
                hex(ord(c))).replace("0x", "\\x") + "{}".format(COLORS['white'])
    print "\n{}[+] Shellcode extracted from byte(s) {:#08x} to {:#08x}:{}".format(COLORS['cyan'], start, end, COLORS['white'])
    print "\n{}\n".format(shellcode)

if __name__ == "__main__":
    """
    main program routine
    """
    __FROM = 0
    __TO = 0

    parser = argparse.ArgumentParser()
    parser.add_argument("file", help="Specify a file")
    parser.add_argument(
        "-d", "--decimal", help="Display DEC values with HEX", action="store_true")
    parser.add_argument(
        "-s", "--start", help="Start byte")
    parser.add_argument(
        "-e", "--end", help="End byte")
    parser.add_argument(
        "-D", "--diff", help="Perform diff with FILENAME")
    parser.add_argument(
        "-S", "--shellcode", help="Extract shellcode (-s and -e has to be passed)", action="store_true")

    args = parser.parse_args()
    b = 16

    # for -D / --diff - second file has to be opened
    # https://github.com/bl4de/security-tools/issues/22 [RESOLVED]
    if args.diff:
        diff_file = open(args.diff, 'rb')

    if args.file:
        # read first 8 bytes to recognize file type
        print file_type(open(args.file, 'rb').read(8))

        with open(args.file, 'rb') as infile:
            if args.start > -1 and args.end and (int(args.start, 16) > -1 and int(args.end, 16) > int(args.start, 16)):
                __FROM = int(args.start, 16)
                __TO = int(args.end, 16)
            else:
                __TO = os.path.getsize(args.file)

            if args.shellcode and __FROM > -1 and __TO:
                extract_shellcode(__FROM, __TO, infile)

            infile.seek(__FROM)

            if args.diff:
                diff_file.seek(__FROM)

            offset = __FROM

            print "{}[+] Hex dump: {}\n".format(COLORS['cyan'], COLORS['white'])
            while offset < __TO:
                chunk = infile.read(b)

                if args.diff:
                    df_chunk = diff_file.read(b)
                else:
                    df_chunk = False

                if len(chunk) == 0:
                    break

                text = str(chunk)
                text = ''.join([format_text(i) for i in text])

                output = "{}{:#08x}{}".format(
                    COLORS['cyan'], offset, COLORS['white']) + ": "

                output += format_chunk(chunk, 0, 4,
                                       df_chunk, args.decimal) + " | "
                output += format_chunk(chunk, 4, 8,
                                       df_chunk, args.decimal) + " | "
                output += format_chunk(chunk, 8, 12,
                                       df_chunk, args.decimal) + " | "
                output += format_chunk(chunk, 12, 16, df_chunk, args.decimal)

                if args.diff:
                    df_text = str(df_chunk)
                    df_text = ''.join([format_text(i) for i in df_text])

                    df_output = "    " + \
                        format_chunk(df_chunk, 0, 4, chunk,
                                     args.decimal) + " | "
                    df_output += format_chunk(df_chunk,
                                              4, 8, chunk, args.decimal) + " | "
                    df_output += format_chunk(df_chunk,
                                              8, 12, chunk, args.decimal) + " | "
                    df_output += format_chunk(df_chunk, 12,
                                              16, chunk, args.decimal) + df_text

                if len(chunk) % b != 0:
                    if args.decimal:
                        output += "   " * (((b * 2) - 4 - len(chunk))) + text
                        if args.diff:
                            df_output += "   " * \
                                (((b * 2) - 4 - len(df_chunk))) + df_text
                    else:
                        output += "   " * (b + 4 - len(chunk)) + text
                        if args.diff:
                            df_output += "   " * \
                                (b + 4 - len(df_chunk)) + df_text
                else:
                    output += " " + text
                    if args.diff:
                        output += df_output

                print output
                offset += 16

            print
    else:
        print parser.usage
