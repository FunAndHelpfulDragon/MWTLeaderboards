use std::process::ExitCode;

use tokio;

mod leaderboard;

#[tokio::main]
async fn main() -> ExitCode {
    ExitCode::SUCCESS
}
