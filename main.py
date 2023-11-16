
import { CreateAxiosProxy } from '../../utils/proxyAgent';
import es from 'event-stream';
import { Event, EventStream, parseJSON } from '../../utils';

interface Message {
  role: string;
  content: string;
}

interface RealReq {
  messages: Message[];
