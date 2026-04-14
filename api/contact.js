export default async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    const { name, email, phone, message } = req.body;

    if (!name || !email) {
      return res.status(400).json({ error: 'Name and email are required' });
    }

    // TODO: Integrate with n8n webhook
    // const n8nWebhookUrl = process.env.N8N_WEBHOOK_URL;
    // if (n8nWebhookUrl) {
    //   await fetch(n8nWebhookUrl, {
    //     method: 'POST',
    //     headers: { 'Content-Type': 'application/json' },
    //     body: JSON.stringify({ name, email, phone, message, timestamp: new Date().toISOString() }),
    //   });
    // }

    return res.status(200).json({ success: true, message: 'Form submitted successfully' });
  } catch (error) {
    return res.status(500).json({ error: 'Internal server error' });
  }
}
