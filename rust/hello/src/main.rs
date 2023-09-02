use rand::Rng; // randクレートを使用して乱数を生成

fn main() {
    // 乱数生成器を初期化
    let mut rng = rand::thread_rng();
    
    // 1から6の範囲でランダムな整数を生成
    let roll = rng.gen_range(1..=6);
    
    println!("サイコロの目: {}", roll);
}
