# Container, native-host and job baseline

## Placement decision
OpenWrt/firewall4/dnsmasq/odhcpd/LuCI/uHTTPd/Dropbear run as firmware services. Proxmox/QEMU and Debian host management, systemd/networkd/SSH/time, disk and UPS management remain supported native components. Asterisk preferably has a dedicated Debian VM for SIP/RTP/NAT. KeePassXC is an offline workstation tool. Do not hide these privileged responsibilities inside a privileged omnibus container.

Applications and bounded workers use Debian guests and Podman + Quadlet + systemd where compatible. CLI tools, libraries, PHP, pgvector, Asterisk modules and model weights are dependencies or jobs, not new permanent microservices. Conditional/external/legacy records retain their original status. Native app schedulers stay native, including Postiz Temporal and Mautic queues. Production Docker Compose recipes require reviewed translation, not blind execution.

## Required component manifest
Record exact upstream/version/license and image digest; build provenance/SBOM; architecture; process UID/GID and rootless user namespace; all runtime dependencies; network ingress/egress; native DB/cache assignments; persistent volume schema/ownership; secret references; resource ceilings; liveness/readiness; boot order versus application readiness; queue/drain behavior; backup/restore/retention; migration and rollback; current vulnerabilities/exceptions.

## Container hardening
Use non-root application processes, drop all capabilities unless narrowly justified, `NoNewPrivileges=true`, default seccomp and applicable AppArmor/SELinux. Read-only root filesystem with explicitly writable state and bounded tmpfs. No host network/PID/IPC, host sockets, SSH agent, container engine socket, `/`/home/private key mounts or arbitrary device passthrough. Do not pass secrets in image ARG/ENV, build layers or logged CLI strings. Prefer mounted secret files; where a product requires environment credentials, document the exposure and restrict process inspection and logs.

Pin images by registry/repository digest, prefetch in a controlled step, and scan the exact digest. Resource accounting covers CPU, memory, PIDs, disk/temp/output size, GPU device and VRAM quotas; a GPU flag alone is not isolation. Rootless cgroup limits depend on host support: validate cgroup v2/delegation and actual enforcement. Do not remove limits to make a test green.

Quadlet units use the correct rootless user search path and user systemd manager; a `[Service] User=` assignment is not how to turn a rootful Quadlet into rootless. Confirm supported options with the installed generator and dry-run output. Health and readiness differ; dependency ordering alone does not make a database ready. Bounded startup grace/retries are mandatory. Never force an arbitrary unsupported DB version or Valkey replacement.

## Egress and public exposure
Databases, caches, ARI, management dashboards, agent controller and hypervisor interfaces are private. Bind only intentional web ingress through Caddy. An internal Podman network may limit routing but is not a complete tenant or host firewall. Prove IPv4/IPv6, DNS, proxy, VPN and link-local/cloud metadata deny policies from each execution zone. Browser/media/model inputs are untrusted. Provider integration needs explicit approved account, scope, limits and final guards; the network path alone grants no business permission.

## Agent and integration test isolation
Agents edit fresh snapshots. Host-side controls validate symlinks, traversal, file types, file size and path scope before any result is imported. Agents never run with the production Ansible inventory/keyring or deploy token. Native service integration tests run on disposable engineering VMs or approved ephemeral runners with fake credentials and denied real provider egress. Nested privileged Docker/Podman in an agent is forbidden. Kubernetes, a new global Temporal deployment or a message broker is not introduced by this package.

## Operational tests
Test deny paths, enforced memory/PID/time limits, graceful shutdown, queue draining, dependency outage, credential rotation, coherent backup/restore, held resume, restart after power loss and rollback with external side-effect reconciliation. Component packaging acceptance and actual site acceptance are distinct. Example templates in this repository are deliberately not installable until their digest/path/secret placeholders have been supplied and reviewed.
