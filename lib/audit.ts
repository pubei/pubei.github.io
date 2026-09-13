// 活动日志工具 - 异步写入审计日志，不阻塞主流程
import { appendAuditLog } from './kv';
import type { AuditLog } from './types';

let counter = 0;
export async function logAudit(
  action: string,
  module: string,
  target = '',
  detail?: string,
  ip?: string
): Promise<void> {
  try {
    const log: AuditLog = {
      id: `audit_${Date.now()}_${counter++}_${Math.random().toString(36).slice(2, 6)}`,
      action,
      module,
      target,
      detail,
      ip,
      at: Date.now(),
    };
    await appendAuditLog(log);
  } catch {
    // 审计失败不影响主业务
  }
}

// 便捷方法
export const audit = {
  create: (module: string, target: string, detail?: string) => logAudit('create', module, target, detail),
  update: (module: string, target: string, detail?: string) => logAudit('update', module, target, detail),
  remove: (module: string, target: string, detail?: string) => logAudit('delete', module, target, detail),
  login: (target = 'admin') => logAudit('login', 'auth', target),
  logout: (target = 'admin') => logAudit('logout', 'auth', target),
  export: (module: string, target: string, detail?: string) => logAudit('export', module, target, detail),
  import: (module: string, target: string, detail?: string) => logAudit('import', module, target, detail),
  reset: (module: string, target: string, detail?: string) => logAudit('reset', module, target, detail),
};
