# Roles Reference

Built-in role definitions and their permission sets.

## Role Matrix

| Permission | Admin | Analyst | Auditor | ReadOnly | Health | CyberGrid | Reporter | AIUser |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| signals:read | x | x | | x | | | | |
| signals:write | x | x | | | | | | |
| signals:manage | x | | | | | | | |
| observer:read | x | x | | | | | | |
| observer:write | x | x | | | | | | |
| observer:manage | x | | | | | | | |
| reports:read | x | x | x | | | | x | |
| reports:write | x | x | x | | | | | |
| reports:manage | x | | | | | | | |
| frameworks:read | x | x | x | | | | x | |
| frameworks:manage | x | | | | | | | |
| cybergrid:read | x | x | | | | x | | |
| cybergrid:write | x | | | | | x | | |
| cybergrid:manage | x | | | | | x | | |
| health:read | x | | | | x | | | |
| health:manage | x | | | | x | | | |
| metrics:read | x | | | | x | | | |
| settings:read | x | | | | | | | |
| settings:manage | x | | | | | | | |
| ai:read | x | x | | | | | | x |
| ai:write | x | | | | | | | x |
| ai:manage | x | | | | | | | |
| conductor:read | x | | | | | | | |
| conductor:write | x | | | | | | | |
| conductor:admin | x | | | | | | | |
