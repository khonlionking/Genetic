
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
