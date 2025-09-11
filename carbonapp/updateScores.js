import { readFileSync, writeFileSync } from 'fs';

export default function handler(req, res) {
  const file = './scores.json';
  let scores = JSON.parse(readFileSync(file));

  if(req.method === 'POST') {
    const { name, score } = req.body;
    if(name && score !== undefined) {
      scores.push({ name, score });
      // keep only top 20
      scores = scores.sort((a,b)=>b.score-a.score).slice(0,20);
      writeFileSync(file, JSON.stringify(scores));
      return res.status(200).json({ success:true });
    }
  }

  // GET returns leaderboard
  res.status(200).json(scores);
}
