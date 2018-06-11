'use strict'

// some sophisticated function
function bar(arg) {
    return arg + 10
}

// initialize constant
const $BAZ = "heyyy!"

// initialize foo
let __foo = 10

// foo is changed by bar()
__foo = bar(__foo)

// foo = 20
console.log(__foo)