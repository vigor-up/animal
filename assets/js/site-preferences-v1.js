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
  updateCurrency();
})();
