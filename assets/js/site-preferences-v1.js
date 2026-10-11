(() => {
  'use strict';

  const storageKey = 'huolide-site-preferences-v1';
  const currencySelect = document.querySelector('[data-currency-select]');
  const rateInput = document.querySelector('[data-cny-twd-rate]');
  const status = document.querySelector('[data-fx-status]');
  if (!currencySelect || !rateInput) return;

  const isSimplified = document.documentElement.lang === 'zh-CN';
  const numberFormat = new Intl.NumberFormat(isSimplified ? 'zh-CN' : 'zh-TW', {
    maximumFractionDigits: 2
  });
  let rate = NaN;

  function readPreferences() {
    try {
      const saved = JSON.parse(localStorage.getItem(storageKey) || '{}');
      const parsedRate = Number(saved.cnyToTwd);
      if (Number.isFinite(parsedRate) && parsedRate > 0) {
        rate = parsedRate;
        rateInput.value = String(parsedRate);
      }
      if (saved.currency === 'TWD' && Number.isFinite(rate)) {
        currencySelect.value = 'TWD';
      }
    } catch (_) {
      // Keep the page usable when browser storage is unavailable.
    }
  }

  function savePreferences() {
    try {
      localStorage.setItem(storageKey, JSON.stringify({
        currency: currencySelect.value,
        cnyToTwd: Number.isFinite(rate) ? rate : null
      }));
    } catch (_) {
      // The selection still applies to this page without persistent storage.
    }
  }

  function formatValue(cnyAmount, scale) {
    const converted = currencySelect.value === 'TWD' ? cnyAmount * rate : cnyAmount;
    return numberFormat.format(scale > 1 ? converted / scale : converted);
  }

  function updateRoi() {
    const calculator = document.querySelector('[data-roi-calculator]');
    if (!calculator) return;

    const gainInput = calculator.querySelector('[data-roi-gain]');
    const costInput = calculator.querySelector('[data-roi-cost]');
    const headsInput = calculator.querySelector('[data-roi-heads]');
    const statusNode = calculator.querySelector('[data-roi-status]');
    const values = [gainInput, costInput, headsInput].map((input) => input.value.trim());
    const outputs = {
      netHead: calculator.querySelector('[data-roi-net-head]'),
      netBatch: calculator.querySelector('[data-roi-net-batch]'),
      percent: calculator.querySelector('[data-roi-percent]'),
      breakEven: calculator.querySelector('[data-roi-breakeven]')
    };

    calculator.querySelectorAll('[data-roi-currency]').forEach((node) => {
      node.textContent = currencySelect.value;
    });

    const complete = values.every((value) => value !== '' && Number.isFinite(Number(value)) && Number(value) >= 0);
    if (!complete) {
      Object.values(outputs).forEach((node) => { if (node) node.textContent = '—'; });
      if (statusNode) statusNode.textContent = isSimplified
        ? '填入三项自家数据即可试算，数据不会上传。'
        : '填入三項自家數據即可試算，數據不會上傳。';
      return;
    }

    const [gain, cost, heads] = values.map(Number);
    const netPerHead = gain - cost;
    if (outputs.netHead) outputs.netHead.textContent = formatValue(netPerHead, 1);
    if (outputs.netBatch) outputs.netBatch.textContent = formatValue(netPerHead * heads, 1);
    if (outputs.breakEven) outputs.breakEven.textContent = formatValue(gain, 1);
    if (outputs.percent) outputs.percent.textContent = cost > 0
      ? `${numberFormat.format((netPerHead / cost) * 100)}%`
      : (isSimplified ? '成本为 0，不适用' : '成本為 0，不適用');
    if (statusNode) statusNode.textContent = isSimplified
      ? `按当前输入估算：每头净收益 ${formatValue(netPerHead, 1)} ${currencySelect.value}；实际结果以本场记录为准。`
      : `依目前輸入估算：每頭淨收益 ${formatValue(netPerHead, 1)} ${currencySelect.value}；實際結果以本場紀錄為準。`;
  }

  function updateCurrency() {
    const canConvert = Number.isFinite(rate) && rate > 0;
    const twdOption = currencySelect.querySelector('option[value="TWD"]');
    if (twdOption) twdOption.disabled = !canConvert;
    if (!canConvert && currencySelect.value === 'TWD') currencySelect.value = 'CNY';

    const targetCode = currencySelect.value;
    document.querySelectorAll('[data-money]').forEach((node) => {
      const cnyAmount = Number(node.dataset.cny);
      const scale = Number(node.dataset.scale || 1);
      if (!Number.isFinite(cnyAmount) || !Number.isFinite(scale) || scale <= 0) return;
      const prefix = node.dataset.prefix || '';
      const suffix = node.dataset.suffix || '';
      node.textContent = `${prefix}${formatValue(cnyAmount, scale)}${suffix}`;
    });

    document.querySelectorAll('[data-money-unit]').forEach((node) => {
      const unit = targetCode === 'TWD' ? node.dataset.twdUnit : node.dataset.cnyUnit;
      if (unit) node.textContent = unit;
    });
    document.querySelectorAll('[data-money-code]').forEach((node) => {
      node.textContent = targetCode;
    });
    updateRoi();

    if (status) {
      if (canConvert) {
        const displayRate = numberFormat.format(rate);
        status.textContent = isSimplified
          ? `手动汇率：1 CNY = ${displayRate} TWD`
          : `手動匯率：1 CNY = ${displayRate} TWD`;
      } else {
        status.textContent = isSimplified
          ? '输入汇率后可切换 TWD；本站不读取实时汇率。'
          : '輸入匯率後可切換 TWD；本站不讀取即時匯率。';
      }
    }
    savePreferences();
  }

  readPreferences();
  rateInput.addEventListener('input', () => {
    const inputRate = Number(rateInput.value);
    rate = Number.isFinite(inputRate) && inputRate > 0 ? inputRate : NaN;
    updateCurrency();
  });
  currencySelect.addEventListener('change', updateCurrency);
  document.querySelectorAll('[data-roi-gain], [data-roi-cost], [data-roi-heads]').forEach((input) => {
    input.addEventListener('input', updateRoi);
  });
  updateCurrency();
})();
