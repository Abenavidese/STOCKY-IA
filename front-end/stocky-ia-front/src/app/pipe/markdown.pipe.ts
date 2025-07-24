import { Pipe, PipeTransform } from '@angular/core';
import { marked } from 'marked';
import DOMPurify from 'dompurify';

@Pipe({
  name: 'markdown'
})
export class MarkdownPipe implements PipeTransform {
  transform(value: string): string {
    if (!value) return '';
    // Usa marked.parse() para asegurar un string
    const rawHtml = marked.parse(value) as string;
    return DOMPurify.sanitize(rawHtml);
  }
}
