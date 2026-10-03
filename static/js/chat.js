(() => {
  const conversation = document.querySelector("#conversation");
  const chatForm = document.querySelector("#chat-form");
  const messageInput = document.querySelector("#message");
  const orderPanel = document.querySelector("#order-panel");
  const orderForm = document.querySelector("#order-form");
  const selectedProduct = document.querySelector("#selected-product");
  const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;
  let product = null;

  function addMessage(text, kind) {
    const item = document.createElement("article");
    item.className = `message ${kind}`;
    item.textContent = text;
    conversation.append(item);
    conversation.scrollTop = conversation.scrollHeight;
  }

  async function send(url, payload) {
    const response = await fetch(url, {
      method: "POST",
      headers: {"Content-Type": "application/json", "X-CSRFToken": csrfToken},
      body: JSON.stringify(payload),
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.detail || "No pudimos procesar la solicitud.");
    return data;
  }

  chatForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    const text = messageInput.value.trim();
    if (!text) return;
    addMessage(text, "user");
    messageInput.value = "";
    try {
      const result = await send("/chat/message/", {message: text});
      addMessage(result.message, "assistant");
      product = result.product;
      orderPanel.hidden = !product;
      if (product) selectedProduct.textContent = `${product.name} · ${product.presentation} · S/ ${product.price}`;
    } catch (error) {
      addMessage(error.message, "error");
    }
  });

  orderForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    if (!product) return;
    try {
      const result = await send("/orders/request/", {
        product_id: product.id,
        name: document.querySelector("#customer-name").value.trim(),
        phone: document.querySelector("#customer-phone").value.trim(),
        quantity: Number(document.querySelector("#quantity").value),
      });
      addMessage(result.message, "assistant");
      orderForm.reset();
      orderPanel.hidden = true;
      product = null;
    } catch (error) {
      addMessage(error.message, "error");
    }
  });
})();
