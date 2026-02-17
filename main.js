(() => {
  const byId = (id) => document.getElementById(id);

  async function check() {
    const compNumEl = byId('compNum');
    const countryEl = byId('country');
    const resultEl = byId('result');
    const btn = byId('checkBtn');

    const compNum = (compNumEl?.value || '').trim();
    const country = (countryEl?.value || '').trim();

    if (!compNum || !country) {
      resultEl.value = 'Please enter both Comp Number and Country.';
      return;
    }

    if (compNum.length > 3) return alert( 'Comp Number cannot be more than 3 characters.')

    btn.disabled = true;
    resultEl.value = 'Checking...';
    try {
      const res = await fetch('/check', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ compNum, country })
      });
      const data = await res.json();
      if (!res.ok) {
        throw new Error(data && data.error ? data.error : 'Request failed');
      }
      resultEl.value = data.taken ? 'Comp number is TAKEN.' : 'Comp number is NOT taken.';
    } catch (e) {
      resultEl.value = `Error: ${e.message || e}`;
    } finally {
      btn.disabled = false;
    }
  }

  window.addEventListener('DOMContentLoaded', () => {
    const btn = byId('checkBtn');
    if (btn) btn.addEventListener('click', check);
  });
})();
