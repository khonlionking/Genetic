
import { CreateAxiosProxy } from '../../utils/proxyAgent';
import es from 'event-stream';
import { Event, EventStream, parseJSON } from '../../utils';

interface Message {
  role: string;
  content: string;
}

interface RealReq {
  messages: Message[];
  temperature: number;
  stream: boolean;
  model: string;
}

interface OpenAIChatOptions extends ChatOptions {
  base_url?: string;
  api_key?: string;
  proxy?: boolean;
}

export class OpenAI extends Chat {
  private client: AxiosInstance;

  constructor(options?: OpenAIChatOptions) {
    super(options);
    this.client = CreateAxiosProxy(
      {
        baseURL: options?.base_url || 'https://api.openai.com/',
        headers: {
          'Content-Type': 'application/json',
          accept: 'text/event-stream',
          'Cache-Control': 'no-cache',
          'Proxy-Connection': 'keep-alive',
          Authorization: `Bearer ${options?.api_key || ''}`,
        },
      } as CreateAxiosDefaults,
      false,
      !!options?.proxy,
    );
  }

  support(model: ModelType): number {
    return Number.MAX_SAFE_INTEGER;
  }

  public async askStream(req: ChatRequest, stream: EventStream) {
    const data: RealReq = {
      messages: req.messages,
      temperature: 1.0,
      model: req.model,
      stream: true,
    };
    try {
      const res = await this.client.post('/v1/chat/completions', data, {
        responseType: 'stream',
      } as AxiosRequestConfig);
      res.data.pipe(es.split(/\r?\n\r?\n/)).pipe(
        es.map(async (chunk: any, cb: any) => {
          const dataStr = chunk.replace('data: ', '');
          if (!dataStr) {
            return;
          }
          if (dataStr === '[DONE]') {
