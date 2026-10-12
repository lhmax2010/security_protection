#[unsafe(no_mangle)]
#[inline(never)]
pub extern "C" fn secret_transform(x: u32) -> u32 {
    (x ^ 0x5a17).wrapping_mul(33).wrapping_add(7) & 0xffff
}
#[unsafe(no_mangle)]
#[inline(never)]
pub extern "C" fn simple_checksum(s: *const u8, len: usize) -> u32 {
    let mut sum: u32 = 0;
    for i in 0..len { sum = sum.wrapping_mul(31).wrapping_add(unsafe { *s.add(i) } as u32) & 0xffff; }
    sum
}
fn main() {
    let marker = "LICENSE_KEY_CHECK_V1";
    let x = std::env::args().nth(1).and_then(|v| v.parse::<u32>().ok()).unwrap_or(1234);
    println!("{} {} {}", marker, secret_transform(x), simple_checksum(marker.as_ptr(), marker.len()));
}
