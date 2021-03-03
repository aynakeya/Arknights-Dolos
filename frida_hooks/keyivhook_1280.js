function get_func_by_offset(module_name,offset){
    var module=Process.getModuleByName(module_name)
    var addr=module.base.add(offset);
    return new NativePointer(addr.toString());
}

function BinaryToHexString(){
    var func = get_func_by_offset("libil2cpp.so",0x10F6B6D)
    console.log('[+] hook '+func.toString())
    var len = 0;
    Interceptor.attach(func, {
        onEnter: function (args) {
            console.log('******BinaryToHexString********')
            console.log('[index] '+args[2].toInt32())
            console.log('[length] '+args[3].toInt32())
            // len = args[3].toInt32()
            console.log('******BinaryToHexString********')
        },
        onLeave: function (retval) {
            console.log('-------BinaryToHexString-------')
            console.log(retval.readByteArray(len*4+12))
            console.log('-------BinaryToHexString-------')
        }
    });
}

function padding(){
    var func = get_func_by_offset("libil2cpp.so",0x222B3E2)
    console.log('[+] hook '+func.toString())
    Interceptor.attach(func, {
        onEnter: function (args) {
        },
        onLeave: function (retval) {
            console.log('[padding] '+retval.toInt32())
        }
    });
}

function modee(){
    var func = get_func_by_offset("libil2cpp.so",0x222B2AE)
    console.log('[+] hook '+func.toString())
    Interceptor.attach(func, {
        onEnter: function (args) {
        },
        onLeave: function (retval) {
            console.log('[modee] '+retval.toInt32())
        }
    });
}

function ivget(){
    var func = get_func_by_offset("libil2cpp.so",0x222ACE9)
    console.log('[+] hook '+func.toString())
    Interceptor.attach(func, {
        onEnter: function (args) {
        },
        onLeave: function (retval) {
            console.log('[iv get]')
            console.log(retval.readByteArray(16+16))
        }
    });
}

function ivset(){
    var func = get_func_by_offset("libil2cpp.so",0x222ADD3)
    console.log('[+] hook '+func.toString())
    Interceptor.attach(func, {
        onEnter: function (args) {
            console.log('[iv set]')
            console.log(args[1].readByteArray(16+16))
        },
        onLeave: function (retval) {

        }
    });
}

function keyget(){
    var func = get_func_by_offset("libil2cpp.so",0x222AF53)
    console.log('[+] hook '+func.toString())
    Interceptor.attach(func, {
        onEnter: function (args) {
        },
        onLeave: function (retval) {
            console.log('[key get]')
            console.log(retval.readByteArray(16+16))
        }
    });
}

function keyset(){
    var func = get_func_by_offset("libil2cpp.so",0x222B03D)
    console.log('[+] hook '+func.toString())
    Interceptor.attach(func, {
        onEnter: function (args) {
            console.log('[key set]')
            console.log(args[1].readByteArray(16+16+32))
        },
        onLeave: function (retval) {

        }
    });
}

function test2(){
    var func = get_func_by_offset("libil2cpp.so",0x222B56D)
    console.log('[+] hook '+func.toString())
    Interceptor.attach(func, {
        onEnter: function (args) {
            console.log("key")
            console.log(args[1].readByteArray(64));
            console.log("iv")
            console.log(args[2].readByteArray(64));
        },
        onLeave: function (retval) {

        }
    });
}

/*
see https://docs.microsoft.com/en-us/dotnet/api/system.security.cryptography.rijndaelmanaged?view=net-5.0

padding = 2  = PKCS7
ciphermode = 1  = CBC

iv length = 32 in hex = 16 hex pair = 16 in bytes
key length = 32 in hex str = 16 hex pair =  16 in bytes
*/
