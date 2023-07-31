use std::ops::Deref;

use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, PartialEq, PartialOrd, Hash, Serialize, Deserialize)]
pub struct LeaderboardEntry {
    pub(crate) username: String,
    pub(crate) score: i64,
    pub(crate) difference: i64,
}

#[derive(Debug, Clone, PartialEq, PartialOrd, Hash, Serialize, Deserialize)]
pub struct Leaderboard(pub(crate) Vec<LeaderboardEntry>);

#[derive(Debug, Clone, PartialEq, PartialOrd, Hash, Serialize, Deserialize)]
pub struct OCRCleanOutputValue {
    /// username of the person on the leaderboard
    pub(crate) username: String,
    /// rebirth or killstreak count
    pub(crate) score: i64,
}

#[derive(Debug, Clone, PartialEq, PartialOrd, Hash, Serialize, Deserialize)]
pub struct OCRCleanOutput(pub(crate) Vec<OCRCleanOutputValue>);

impl Leaderboard {
    fn find_user<S>(&self, username: S) -> Option<&LeaderboardEntry>
    where
        S: Deref<Target = str>,
    {
        let username = username.deref();
        for el in &self.0 {
            if el.username.eq(username) {
                return Some(&el);
            }
        }

        None
    }

    pub fn from_ocr(&self, ocr: &OCRCleanOutput) -> Leaderboard {
        Leaderboard(
            ocr.0
                .iter()
                .map(|ocr| {
                    LeaderboardEntry::from_old_entry(ocr, self.find_user(ocr.username.deref()))
                })
                .collect(),
        )
    }
}

impl LeaderboardEntry {
    fn from_old_entry(
        ocr: &OCRCleanOutputValue,
        old_leaderboard: Option<&LeaderboardEntry>,
    ) -> LeaderboardEntry {
        LeaderboardEntry {
            username: ocr.username.clone(),
            score: ocr.score,
            difference: match old_leaderboard {
                Some(old) => old.score - ocr.score,
                None => -1,
            },
        }
    }
}
