// Temporary browser-side cart (localStorage) so it survives page changes.
// Team 3 can replace this with a server-side cart; Team 4 builds checkout on top of it.
(function () {
  var KEY = "bookhaven_cart";
  var cart = [];
  try { cart = JSON.parse(localStorage.getItem(KEY)) || []; } catch (e) { cart = []; }

  function save() { try { localStorage.setItem(KEY, JSON.stringify(cart)); } catch (e) {} }

  function render() {
    var count = document.getElementById("cartCount");
    if (count) count.textContent = cart.length;

    var box = document.getElementById("cartItems");
    var totalEl = document.getElementById("cartTotal");
    if (totalEl) {
      totalEl.textContent = "Total: ₹" + cart.reduce(function (s, b) { return s + b.price; }, 0);
    }
    if (!box) return;
    box.textContent = "";
    if (!cart.length) { box.textContent = "Your cart is empty."; return; }

    cart.forEach(function (b, i) {
      var row = document.createElement("div");
      row.className = "d-flex justify-content-between align-items-center border-bottom py-2 gap-2";
      var label = document.createElement("span");
      label.textContent = b.title + " — ₹" + b.price;
      var btn = document.createElement("button");
      btn.className = "small-btn";
      btn.textContent = "Remove";
      btn.addEventListener("click", function () { cart.splice(i, 1); save(); render(); });
      row.appendChild(label);
      row.appendChild(btn);
      box.appendChild(row);
    });
  }

  document.addEventListener("click", function (e) {
    var btn = e.target.closest(".add-to-cart");
    if (!btn) return;
    cart.push({ id: Number(btn.dataset.id), title: btn.dataset.title, price: Number(btn.dataset.price) });
    save();
    render();
  });

  var checkout = document.getElementById("checkoutBtn");
  if (checkout) {
    checkout.addEventListener("click", function () {
      if (!cart.length) { alert("Your cart is empty!"); return; }
      window.location.href = checkout.dataset.url;
     
      
    });
  }

  render();
})();
