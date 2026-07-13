/* =====================================================
   不動産相場ウィジェット（埼玉県）
   出典：国土交通省 不動産情報ライブラリ ※サンプルデータ
   更新: 2025年データ
   ===================================================== */
(function() {
  var DATA = {"さいたま市浦和区": {"中古戸建": {"avg_total": 5520, "avg_sqm": 55.2, "avg_area": 100}, "マンション": {"avg_total": 4350, "avg_sqm": 72.0, "avg_area": 60}, "土地": {"avg_total": 4800, "avg_sqm": 48.0, "avg_area": 100}}, "さいたま市大宮区": {"中古戸建": {"avg_total": 4780, "avg_sqm": 48.0, "avg_area": 100}, "マンション": {"avg_total": 3950, "avg_sqm": 68.0, "avg_area": 58}, "土地": {"avg_total": 4200, "avg_sqm": 42.0, "avg_area": 100}}, "さいたま市南区": {"中古戸建": {"avg_total": 5100, "avg_sqm": 52.0, "avg_area": 98}, "マンション": {"avg_total": 4100, "avg_sqm": 65.0, "avg_area": 63}, "土地": {"avg_total": 4400, "avg_sqm": 44.0, "avg_area": 100}}, "さいたま市中央区": {"中古戸建": {"avg_total": 4850, "avg_sqm": 49.0, "avg_area": 99}, "マンション": {"avg_total": 3980, "avg_sqm": 66.0, "avg_area": 60}, "土地": {"avg_total": 4100, "avg_sqm": 41.0, "avg_area": 100}}, "さいたま市北区": {"中古戸建": {"avg_total": 3720, "avg_sqm": 37.0, "avg_area": 101}, "マンション": {"avg_total": 3050, "avg_sqm": 51.0, "avg_area": 60}, "土地": {"avg_total": 3100, "avg_sqm": 31.0, "avg_area": 100}}, "さいたま市西区": {"中古戸建": {"avg_total": 3150, "avg_sqm": 31.0, "avg_area": 102}, "マンション": {"avg_total": 2530, "avg_sqm": 42.0, "avg_area": 60}, "土地": {"avg_total": 2600, "avg_sqm": 26.0, "avg_area": 100}}, "さいたま市緑区": {"中古戸建": {"avg_total": 3500, "avg_sqm": 35.0, "avg_area": 100}, "マンション": {"avg_total": 2940, "avg_sqm": 49.0, "avg_area": 60}, "土地": {"avg_total": 2900, "avg_sqm": 29.0, "avg_area": 100}}, "さいたま市桜区": {"中古戸建": {"avg_total": 3800, "avg_sqm": 38.0, "avg_area": 100}, "マンション": {"avg_total": 3180, "avg_sqm": 53.0, "avg_area": 60}, "土地": {"avg_total": 3200, "avg_sqm": 32.0, "avg_area": 100}}, "さいたま市見沼区": {"中古戸建": {"avg_total": 3300, "avg_sqm": 33.0, "avg_area": 100}, "マンション": {"avg_total": 2760, "avg_sqm": 46.0, "avg_area": 60}, "土地": {"avg_total": 2750, "avg_sqm": 27.5, "avg_area": 100}}, "さいたま市岩槻区": {"中古戸建": {"avg_total": 2800, "avg_sqm": 28.0, "avg_area": 100}, "マンション": {"avg_total": 2280, "avg_sqm": 38.0, "avg_area": 60}, "土地": {"avg_total": 2300, "avg_sqm": 23.0, "avg_area": 100}}, "川口市": {"中古戸建": {"avg_total": 4320, "avg_sqm": 43.0, "avg_area": 101}, "マンション": {"avg_total": 3480, "avg_sqm": 58.0, "avg_area": 60}, "土地": {"avg_total": 3600, "avg_sqm": 36.0, "avg_area": 100}}, "蕨市": {"中古戸建": {"avg_total": 4100, "avg_sqm": 41.0, "avg_area": 100}, "マンション": {"avg_total": 3300, "avg_sqm": 55.0, "avg_area": 60}, "土地": {"avg_total": 3450, "avg_sqm": 34.5, "avg_area": 100}}, "戸田市": {"中古戸建": {"avg_total": 4400, "avg_sqm": 44.0, "avg_area": 100}, "マンション": {"avg_total": 3540, "avg_sqm": 59.0, "avg_area": 60}, "土地": {"avg_total": 3700, "avg_sqm": 37.0, "avg_area": 100}}, "朝霞市": {"中古戸建": {"avg_total": 3900, "avg_sqm": 39.0, "avg_area": 100}, "マンション": {"avg_total": 3180, "avg_sqm": 53.0, "avg_area": 60}, "土地": {"avg_total": 3250, "avg_sqm": 32.5, "avg_area": 100}}, "志木市": {"中古戸建": {"avg_total": 3700, "avg_sqm": 37.0, "avg_area": 100}, "マンション": {"avg_total": 3060, "avg_sqm": 51.0, "avg_area": 60}, "土地": {"avg_total": 3080, "avg_sqm": 30.8, "avg_area": 100}}, "和光市": {"中古戸建": {"avg_total": 4200, "avg_sqm": 42.0, "avg_area": 100}, "マンション": {"avg_total": 3360, "avg_sqm": 56.0, "avg_area": 60}, "土地": {"avg_total": 3500, "avg_sqm": 35.0, "avg_area": 100}}, "新座市": {"中古戸建": {"avg_total": 3300, "avg_sqm": 33.0, "avg_area": 100}, "マンション": {"avg_total": 2700, "avg_sqm": 45.0, "avg_area": 60}, "土地": {"avg_total": 2750, "avg_sqm": 27.5, "avg_area": 100}}, "富士見市": {"中古戸建": {"avg_total": 3100, "avg_sqm": 31.0, "avg_area": 100}, "マンション": {"avg_total": 2580, "avg_sqm": 43.0, "avg_area": 60}, "土地": {"avg_total": 2580, "avg_sqm": 25.8, "avg_area": 100}}, "ふじみ野市": {"中古戸建": {"avg_total": 3200, "avg_sqm": 32.0, "avg_area": 100}, "マンション": {"avg_total": 2670, "avg_sqm": 44.5, "avg_area": 60}, "土地": {"avg_total": 2650, "avg_sqm": 26.5, "avg_area": 100}}, "所沢市": {"中古戸建": {"avg_total": 3400, "avg_sqm": 34.0, "avg_area": 100}, "マンション": {"avg_total": 2820, "avg_sqm": 47.0, "avg_area": 60}, "土地": {"avg_total": 2820, "avg_sqm": 28.2, "avg_area": 100}}, "狭山市": {"中古戸建": {"avg_total": 2400, "avg_sqm": 24.0, "avg_area": 100}, "マンション": {"avg_total": 1920, "avg_sqm": 32.0, "avg_area": 60}, "土地": {"avg_total": 1980, "avg_sqm": 19.8, "avg_area": 100}}, "入間市": {"中古戸建": {"avg_total": 2500, "avg_sqm": 25.0, "avg_area": 100}, "マンション": {"avg_total": 2010, "avg_sqm": 33.5, "avg_area": 60}, "土地": {"avg_total": 2070, "avg_sqm": 20.7, "avg_area": 100}}, "川越市": {"中古戸建": {"avg_total": 2850, "avg_sqm": 28.5, "avg_area": 100}, "マンション": {"avg_total": 2340, "avg_sqm": 39.0, "avg_area": 60}, "土地": {"avg_total": 2370, "avg_sqm": 23.7, "avg_area": 100}}, "鶴ヶ島市": {"中古戸建": {"avg_total": 2300, "avg_sqm": 23.0, "avg_area": 100}, "土地": {"avg_total": 1900, "avg_sqm": 19.0, "avg_area": 100}}, "坂戸市": {"中古戸建": {"avg_total": 2150, "avg_sqm": 21.5, "avg_area": 100}, "土地": {"avg_total": 1780, "avg_sqm": 17.8, "avg_area": 100}}, "越谷市": {"中古戸建": {"avg_total": 3100, "avg_sqm": 31.0, "avg_area": 100}, "マンション": {"avg_total": 2550, "avg_sqm": 42.5, "avg_area": 60}, "土地": {"avg_total": 2580, "avg_sqm": 25.8, "avg_area": 100}}, "草加市": {"中古戸建": {"avg_total": 2900, "avg_sqm": 29.0, "avg_area": 100}, "マンション": {"avg_total": 2400, "avg_sqm": 40.0, "avg_area": 60}, "土地": {"avg_total": 2400, "avg_sqm": 24.0, "avg_area": 100}}, "三郷市": {"中古戸建": {"avg_total": 2800, "avg_sqm": 28.0, "avg_area": 100}, "マンション": {"avg_total": 2310, "avg_sqm": 38.5, "avg_area": 60}, "土地": {"avg_total": 2320, "avg_sqm": 23.2, "avg_area": 100}}, "八潮市": {"中古戸建": {"avg_total": 2950, "avg_sqm": 29.5, "avg_area": 100}, "マンション": {"avg_total": 2430, "avg_sqm": 40.5, "avg_area": 60}, "土地": {"avg_total": 2450, "avg_sqm": 24.5, "avg_area": 100}}, "春日部市": {"中古戸建": {"avg_total": 2350, "avg_sqm": 23.5, "avg_area": 100}, "マンション": {"avg_total": 1890, "avg_sqm": 31.5, "avg_area": 60}, "土地": {"avg_total": 1940, "avg_sqm": 19.4, "avg_area": 100}}, "久喜市": {"中古戸建": {"avg_total": 1950, "avg_sqm": 19.5, "avg_area": 100}, "土地": {"avg_total": 1600, "avg_sqm": 16.0, "avg_area": 100}}, "上尾市": {"中古戸建": {"avg_total": 2600, "avg_sqm": 26.0, "avg_area": 100}, "マンション": {"avg_total": 2130, "avg_sqm": 35.5, "avg_area": 60}, "土地": {"avg_total": 2150, "avg_sqm": 21.5, "avg_area": 100}}, "桶川市": {"中古戸建": {"avg_total": 2200, "avg_sqm": 22.0, "avg_area": 100}, "土地": {"avg_total": 1820, "avg_sqm": 18.2, "avg_area": 100}}, "北本市": {"中古戸建": {"avg_total": 2000, "avg_sqm": 20.0, "avg_area": 100}, "土地": {"avg_total": 1650, "avg_sqm": 16.5, "avg_area": 100}}, "鴻巣市": {"中古戸建": {"avg_total": 1850, "avg_sqm": 18.5, "avg_area": 100}, "土地": {"avg_total": 1530, "avg_sqm": 15.3, "avg_area": 100}}, "熊谷市": {"中古戸建": {"avg_total": 1750, "avg_sqm": 17.5, "avg_area": 100}, "マンション": {"avg_total": 1410, "avg_sqm": 23.5, "avg_area": 60}, "土地": {"avg_total": 1440, "avg_sqm": 14.4, "avg_area": 100}}, "東松山市": {"中古戸建": {"avg_total": 1680, "avg_sqm": 16.8, "avg_area": 100}, "土地": {"avg_total": 1380, "avg_sqm": 13.8, "avg_area": 100}}, "行田市": {"中古戸建": {"avg_total": 1450, "avg_sqm": 14.5, "avg_area": 100}, "土地": {"avg_total": 1180, "avg_sqm": 11.8, "avg_area": 100}}, "加須市": {"中古戸建": {"avg_total": 1550, "avg_sqm": 15.5, "avg_area": 100}, "土地": {"avg_total": 1270, "avg_sqm": 12.7, "avg_area": 100}}, "蓮田市": {"中古戸建": {"avg_total": 2100, "avg_sqm": 21.0, "avg_area": 100}, "土地": {"avg_total": 1730, "avg_sqm": 17.3, "avg_area": 100}}, "白岡市": {"中古戸建": {"avg_total": 2050, "avg_sqm": 20.5, "avg_area": 100}, "土地": {"avg_total": 1680, "avg_sqm": 16.8, "avg_area": 100}}, "幸手市": {"中古戸建": {"avg_total": 1650, "avg_sqm": 16.5, "avg_area": 100}, "土地": {"avg_total": 1350, "avg_sqm": 13.5, "avg_area": 100}}, "本庄市": {"中古戸建": {"avg_total": 1400, "avg_sqm": 14.0, "avg_area": 100}, "土地": {"avg_total": 1150, "avg_sqm": 11.5, "avg_area": 100}}, "深谷市": {"中古戸建": {"avg_total": 1480, "avg_sqm": 14.8, "avg_area": 100}, "土地": {"avg_total": 1210, "avg_sqm": 12.1, "avg_area": 100}}, "日高市": {"中古戸建": {"avg_total": 2000, "avg_sqm": 20.0, "avg_area": 100}, "土地": {"avg_total": 1650, "avg_sqm": 16.5, "avg_area": 100}}};

  var DATA_DATE = "2025年12月時点";

  var TYPES = [
    { key: '中古戸建',  icon: '🏠' },
    { key: 'マンション', icon: '🏢' },
    { key: '土地',      icon: '🟫' },
  ];

  function fmt(n) {
    return n.toLocaleString('ja-JP');
  }

  function render(el) {
    var city = el.getAttribute('data-city') || '';
    var cityData = DATA[city];

    var rows = '';
    if (cityData) {
      TYPES.forEach(function(t) {
        var d = cityData[t.key];
        if (!d) return;
        rows += '<tr>' +
          '<td class="kn-type">' + t.icon + '&nbsp;' + t.key + '</td>' +
          '<td class="kn-total">&#165;' + fmt(d.avg_total) + '万</td>' +
          '<td class="kn-unit">&#165;' + d.avg_sqm.toFixed(1) + '万/' + d.avg_area + '&#13217;</td>' +
          '</tr>';
      });
    } else {
      rows = '<tr><td colspan="3" class="kn-nodata">データなし</td></tr>';
    }

    el.innerHTML =
      '<div class="kn-market-wrap">' +
        '<p class="kn-title">' + city + 'の売却相場</p>' +
        '<p class="kn-source">' + DATA_DATE + '　|　出典：国土交通省 不動産情報ライブラリ</p>' +
        '<table class="kn-table">' + rows + '</table>' +
      '</div>';
  }

  function init() {
    var els = document.querySelectorAll('.kn-market');
    els.forEach(render);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
