import { useState, useEffect } from "react";
import { createBrand, getMentions, getSummary } from "./api";
import { Line } from "react-chartjs-2";
import 'chart.js/auto';
import {
  Box, Button, TextField, Card, CardContent, Typography, Chip
} from "@mui/material";

function parseBuckets(buckets) {
  if (!buckets || typeof buckets !== "object") {
    return {label: [], data: []};
  }
  const entries = Object.entries(buckets).sort((a, b) => 
    a[0] > b[0] ? 1 : -1
  );

  return {
    labels: entries.map(([ts]) => 
      new Date(ts).toLocaleTimeString()
    ),
    data: entries.map(([, count]) => count)
  };
}

export default function App() {
  const [brand, setBrand] = useState("YourBrand");
  const [summary, setSummary] = useState(null);
  const [mentions, setMentions] = useState([]);
  const [poll, setPoll] = useState(true);

  useEffect(() => {
    let interval;

    const fetchData = async () => {
      if (!brand.trim()) {
        setSummary(null);
        setMentions([]);
        return;
      }
      try {
        const s = await getSummary(brand.trim());
        setSummary(s.data);

        const m = await getMentions(brand.trim());
        setMentions(m.data);
      } catch (e) {
        console.error("Error fetching data:", e);
      }
    };

    fetchData();

    if (poll) {
      interval = setInterval(fetchData, 5000);
    }

    return () => clearInterval(interval);
  }, [brand, poll]);

  const handleTrack = async () => {
    await createBrand(brand);
    console.log("Tracking brand:", brand);
  };

  const chart = summary ? parseBuckets(summary.buckets) : {labels: [], data: []};

  const chartData = {
    labels: chart.labels,
    datasets: [
      {
        label: "Mentions per Minute",
        data: chart.data,
        fill: true,
        tension: 0.3
      }
    ]
  };

  return (
    <Box sx={{padding: 3}}>
      <Box sx={{display: "flex", gap: 2, marginBottom: 3}}>
        <TextField 
          label="Brand"
          value={brand}
          onChange={(e) => setBrand(e.target.value)}
        />
        <Button variant="contained" onClick={handleTrack}>
          Track
        </Button>
        <Button variant="outlined" onClick={() => setPoll(!poll)}>
          {poll ? "Pause": "Resume"}
        </Button>
      </Box>

      <Box sx={{display:"grid", gridTemplateColumns: "2fr 1fr", gap: 2}}>
        <Card>
          <CardContent>
            <Typography variant="h6">Mentions Timeline</Typography>
            <Line data={chartData} />
          </CardContent>
        </Card>

        <Card>
          <CardContent>
            <Typography variant="h6">Sentiment</Typography>
            {summary && 
                summary?.sentiment?.map((s) => (
                  <Chip key={s.sentiment} label={`${s.sentiment}: ${s.count}`} sx={{m: 0.5}} />
            ))}

            <Typography variant="h6" sx={{marginTop: 2}}>
              Alerts
            </Typography>
            {summary && summary?.alerts?.length === 0 && (
              <Typography>No Alerts</Typography>
            )}
            {summary && summary?.alerts?.map((a) => (
              <Typography key={a.id}>{a.type}: {a.message}</Typography>
            ))}
          </CardContent>
        </Card>
      </Box>

      <Box sx={{marginTop: 3}}>
        <Typography variant="h6">Recent Mentions</Typography>
        {mentions?.map((m) => (
          <Card key={m.id} sx={{ marginBottom: 1}}>
            <CardContent>
              <Typography variant="subtitle2">
                {m.source} • {new Date(m.published_at).toLocaleDateString()}
              </Typography>
              <Typography>{m.text}</Typography>
              <Chip label={m.sentiment} sx={{marginTop: 1}} />
            </CardContent>
          </Card>
        ))}
      </Box>
    </Box>
  )
}
