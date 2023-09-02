use rand::Rng; // randクレーとを入れる

fn main() {
    let mut rng = rand::thread_rng();

    let num_rolls = 1;

    for _ in 0..num_rolls {
        // 1から6までのランダムな整数を生成
        let roll_result = rng.gen_range(1..=6);
        
        println!("サイコロの目: {}", roll_result);
    }
}
