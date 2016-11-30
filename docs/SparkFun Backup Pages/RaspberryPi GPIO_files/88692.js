// find this script
var target_script;
var scripts = document.getElementsByTagName('script');
for (var i=0; i<scripts.length; i++) {
  if (scripts[i].src == 'https://www.sparkfun.com/wish_lists/88692.js') {
    target_script = scripts[i];
    break;
  }
}
var target_parent = target_script.parentNode;

// css
var styles = document.createElement('link');
styles.rel = 'stylesheet';
styles.type = 'text/css';
styles.href = 'https://www.sparkfun.com/css/embed/wish_list.css';
target_parent.insertBefore(styles, target_script);

// wrapper for innerHTML
var wrapper = document.createElement('div');

var html = '<div id="wish-list-88692" class="sfe-wish-list">';

html += '<div class="sfe-title"><a href="https://www.sparkfun.com/wish_lists/88692"><strong>Raspberry gPIo</strong> <span class="sfewl">SparkFun Wish List</span></a>';

// only show add to cart if on sparkfun.com
if (document.domain.match(/sparkfun\.com/)) {
  html += '<form action="https://www.sparkfun.com/wish_lists/88692/dump" method="post"><input type=submit value="Add all to cart" class="btn btn-default" /></form>';
}

html += '</div>';

html += '<div class="sfe-inner"><div class="sfe-row"><a href="https://www.sparkfun.com/products/11546"><img width="58" height="58" class="sfe-thumbnail" src="https://cdn.sparkfun.com/r/58-58/assets/parts/7/4/9/7/11546-01.jpg" /><span class="sfe-text"><span class="sfe-item-title">Raspberry Pi - Model B <span class="sfe-sku"><span class="sfe-stock sfe-stock-retired" title="Retired"></span> DEV-11546</span></span><span class="sfe-description">Who wants pi? The Raspberry Pi has made quite a splash since it was first announced. The credit-card sized computer is capable of many of the things t&hellip;</span></span></a></div><div class="sfe-row"><a href="https://www.sparkfun.com/products/12652"><img width="58" height="58" class="sfe-thumbnail" src="https://cdn.sparkfun.com/r/58-58/assets/parts/9/3/5/2/12652-01a.jpg" /><span class="sfe-text"><span class="sfe-item-title">SparkFun Pi Wedge <span class="sfe-sku"><span class="sfe-stock sfe-stock-retired" title="Retired"></span> KIT-12652</span></span><span class="sfe-description">This is the SparkFun Pi Wedge, a small board that connects to the Raspberry Pi\'s 26-pin GPIO connector, and breaks the pins out to breadboard-friendly&hellip;</span></span></a></div><div class="sfe-row"><a href="https://www.sparkfun.com/products/12002"><img width="58" height="58" class="sfe-thumbnail" src="https://cdn.sparkfun.com/r/58-58/assets/parts/8/5/0/3/12002-04.jpg" /><span class="sfe-text"><span class="sfe-item-title">(2) Breadboard - Self-Adhesive (White) <span class="sfe-sku"><span class="sfe-stock sfe-stock-in" title="in stock"></span> PRT-12002</span></span><span class="sfe-description">This is your tried and true white solderless breadboard. It has 2 power buses, 10 columns, and 30 rows - a total of 400 tie in points. All pins are sp&hellip;</span></span></a></div><div class="sfe-row"><a href="https://www.sparkfun.com/products/11026"><img width="58" height="58" class="sfe-thumbnail" src="https://cdn.sparkfun.com/r/58-58/assets/parts/3/7/0/4/11026-02.jpg" /><span class="sfe-text"><span class="sfe-item-title">Jumper Wires Standard 7&quot; M/M - 30 AWG (30 Pack) <span class="sfe-sku"><span class="sfe-stock sfe-stock-in" title="in stock"></span> PRT-11026</span></span><span class="sfe-description">If you need to knock up a quick prototype there\'s nothing like having a pile of jumper wires to speed things up, and let\'s face it: sometimes you want&hellip;</span></span></a></div><div class="sfe-row"><a href="https://www.sparkfun.com/products/9190"><img width="58" height="58" class="sfe-thumbnail" src="https://cdn.sparkfun.com/r/58-58/assets/parts/2/6/2/9/09190-03-L.jpg" /><span class="sfe-text"><span class="sfe-item-title">Momentary Pushbutton Switch - 12mm Square <span class="sfe-sku"><span class="sfe-stock sfe-stock-in" title="in stock"></span> COM-09190</span></span><span class="sfe-description">This is a standard 12mm square momentary button. What we really like is the large button head and good tactile feel (it \'clicks\' really well). This bu&hellip;</span></span></a></div><div class="sfe-row"><a href="https://www.sparkfun.com/products/11507"><img width="58" height="58" class="sfe-thumbnail" src="https://cdn.sparkfun.com/r/58-58/assets/parts/7/4/1/7/11507-02.jpg" /><span class="sfe-text"><span class="sfe-item-title">Resistor 330 Ohm 1/6 Watt PTH - 20 pack <span class="sfe-sku"><span class="sfe-stock sfe-stock-in" title="in stock"></span> COM-11507</span></span><span class="sfe-description">1/6 Watt, +/- 5% tolerance PTH resistors. Commonly used in breadboards and perf boards, these 330Ohm resistors make excellent LED current limiters and&hellip;</span></span></a></div><div class="sfe-row"><a href="https://www.sparkfun.com/products/9590"><img width="58" height="58" class="sfe-thumbnail" src="https://cdn.sparkfun.com/r/58-58/assets/parts/3/3/8/0/09590-01.jpg" /><span class="sfe-text"><span class="sfe-item-title">LED - Basic Red 5mm <span class="sfe-sku"><span class="sfe-stock sfe-stock-in" title="in stock"></span> COM-09590</span></span><span class="sfe-description">LEDs - those blinky things. A must have for power indication, pin status, opto-electronic sensors, and fun blinky displays.   This is a very basic 5mm&hellip;</span></span></a></div>';

html += '<div class="sfe-footer"><a class="button" href="https://www.sparkfun.com/wish_lists/88692">View <strong>Raspberry gPIo</strong> on SparkFun.com</a></div>';

html += '</div>'; // end .sfe-inner

html += '</div>'; // end .sfe-wish-list

wrapper.innerHTML = html;

target_parent.insertBefore(wrapper, target_script);
