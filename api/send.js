export default async function handler(req, res) {
  const instanceId = process.env.INSTANCE_ID;
  const token = process.env.TOKEN;
  const phone = process.env.PHONE;
  const mensagem = process.env.MENSAGEM;

  const url = `https://api.z-api.io/instances/${instanceId}/token/${token}/send-text`;

  try {
    const response = await fetch(url, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        phone: phone,
        message: mensagem
      })
    });

    const data = await response.json();

    // Retorna o resultado da API
    return res.status(200).json({ success: true, data });
  } catch (error) {
    return res.status(500).json({ success: false, error: error.message });
  }
}
