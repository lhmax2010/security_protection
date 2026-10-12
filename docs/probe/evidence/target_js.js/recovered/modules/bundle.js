function secret_transform(x) {
    return (x ^ 23063) * 33 + 7 & 65535;
}
function simple_checksum(s) {
    let total = 0;
    for (const b of Buffer.from(s, 'ascii')){
        total = total * 31 + b & 65535;
    }
    return total;
}
const marker = 'LICENSE_KEY_CHECK_V1';
const x = process.argv.length > 2 ? Number(process.argv[2]) >>> 0 : 1234;
console.log(marker, secret_transform(x), simple_checksum(marker));
export default {
    secret_transform,
    simple_checksum
};
