import Anthropic from '@anthropic-ai/sdk'

const client = new Anthropic({ apiKey: process.env.ANTHROPIC_API_KEY })

export default async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' })
  }

  const { messages } = req.body
  if (!messages || !Array.isArray(messages)) {
    return res.status(400).json({ error: 'messages required' })
  }

  try {
    const response = await client.messages.create({
      model: 'claude-opus-4-8',
      max_tokens: 1024,
      system: `당신은 펫미용샵 창업 전문 컨설턴트입니다. 한국어로 친절하고 전문적으로 답변하세요.
펫미용샵 창업에 관한 질문(인허가, 자격증, 입지 선정, 운영, 마케팅, 재무, 국가 지원 등)에
구체적이고 실용적인 조언을 제공하세요. 답변은 간결하게 유지하세요.`,
      messages,
    })

    const text = response.content.find(b => b.type === 'text')?.text ?? ''
    res.status(200).json({ text })
  } catch (err) {
    console.error(err)
    res.status(500).json({ error: '서버 오류가 발생했습니다.' })
  }
}
