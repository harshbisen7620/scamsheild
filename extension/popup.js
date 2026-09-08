document.addEventListener('DOMContentLoaded', () => {
  const analyzeBtn = document.getElementById('analyzeBtn');

  analyzeBtn.addEventListener('click', async () => {
    const text = document.getElementById('inputText').value;
    if (!text) return alert("Kripya pehle text dalein!");

    analyzeBtn.innerText = "Analyzing...";
    analyzeBtn.disabled = true;

    const formData = new FormData();
    formData.append('text', text);

    try {
      const res = await fetch('http://localhost:8000/analyze', { 
        method: 'POST', 
        body: formData 
      });

      if (!res.ok) {
        throw new Error(`Server Error: ${res.status}`);
      }

      const data = await res.json();

      document.getElementById('scoreDisplay').innerText = `${data.verdict} (${data.risk_score}%)`;
      document.getElementById('scoreDisplay').className = `score ${data.risk_score > 50 ? 'high' : 'safe'}`;
      
      document.getElementById('reasonsList').innerHTML = data.reasons.map(r => `<li>${r}</li>`).join('');
      document.getElementById('actionList').innerHTML = data.action_plan.map(a => `<li>${a}</li>`).join('');
      document.getElementById('result').style.display = 'block';

    } catch (err) {
      console.error("Fetch Error:", err);
      alert("Backend connect nahi ho paya! Console (F12) check karein.");
    } finally {
      analyzeBtn.innerText = "Analyze";
      analyzeBtn.disabled = false;
    }
  });
});