# Automated IT Infrastructure Monitoring with Ansible, Prometheus, and Grafana

A streamlined approach to proactively monitor, visualize, and alert on system performance across multiple servers. This setup leverages **Ansible** for automation, **Prometheus** for metrics collection, **Alertmanager** for alerts, **Grafana** for visualization, **MySQL** for storing logs, and a **Python** script for extracting and inserting logs into the database.

## Project Objective
- Deploy an automated monitoring and log management system.
- Receive real-time metrics and visualizations.
- Send automatic alerts for system anomalies.

## Scope
1. Automate the deployment of Prometheus, Grafana, and Node Exporter with Ansible.
2. Collect and store logs in MySQL via Python.
3. Configure Prometheus Alertmanager for email notifications.
4. Visualize data in Grafana dashboards.

## High-Level Steps

### 1. Set Up AWS EC2 Instances
- Spin up four Ubuntu-based EC2s (one **controller**, three **workers**).
- Note both public and private IP addresses.
- Configure security groups to allow relevant ports (e.g., 22 for SSH, 9090 for Prometheus, 9093 for Alertmanager, 3000 for Grafana).

### 2. Configure SSH Access
- Use PuTTY (or similar) to connect and rename each instance (controller, worker1, worker2, worker3).
- Update `/etc/hosts` on each machine with private IP addresses.
- Enable root login and password authentication in `sshd_config`, then restart SSH.
- Set a password for each instance and verify connectivity between machines (ping).

### 3. Install and Configure Ansible (Controller Only)
- Generate SSH keys on the controller, then copy them to the workers (`ssh-copy-id`).
- Install Ansible on the controller:
  ```bash
  sudo apt update
  sudo apt install ansible
  ```
- Create an inventory (`hosts`) file listing the workers.
- Test connectivity with:
  ```bash
  ansible -i hosts all -m ping
  ```

### 4. Set Up MySQL Database
- Install MySQL and Python dependencies on the controller:
  ```bash
  sudo apt install mysql-server python3-pip -y
  ```
- Create a database (`system_metrics`), user (`metrics_user`), and grant permissions.
- Edit `mysqld.cnf` to allow remote access (bind-address = 0.0.0.0).

### 5. Ansible Playbook for Metrics Collection
- Create a playbook (e.g., `metrics.yaml`) that:
  1. Installs Python dependencies (psutil, mysql-connector).
  2. Copies a Python script (`linux_metrics.py`) onto each worker.
  3. Sets up a cron job to run the script periodically (e.g., every minute).
- Verify and execute the playbook with:
  ```bash
  ansible-playbook -i hosts metrics.yaml
  ```

### 6. Prometheus Installation
- Download and extract Prometheus:
  ```bash
  wget https://github.com/prometheus/prometheus/releases/download/v2.53.3/prometheus-2.53.3.linux-amd64.tar.gz
  ```
- Move files to appropriate directories (e.g., `/etc/Prometheus`).
- Create a Prometheus service and start it.
- Access the Prometheus UI at `http://<controller-ip>:9090`.

### 7. Install and Configure Node Exporter
- Deploy with Ansible on worker nodes to collect CPU, memory, and disk metrics.
- Update `prometheus.yml` with the new scrape targets (worker IPs) and restart Prometheus.

### 8. Alertmanager Configuration
- Download and configure Alertmanager to handle alerts from Prometheus.
- Define alerting rules (e.g., missing Node Exporter).
- Configure email or other notification routes (requires email app password).
- Access Alertmanager UI at `http://<controller-ip>:9093`.

### 9. Grafana Installation
- Install Grafana:
  ```bash
  sudo apt-get install grafana
  ```
- Enable and start the Grafana service (`systemctl enable grafana-server`).
- Access the UI at `http://<controller-ip>:3000` (default login: `admin/admin`).
- Add **MySQL** and **Prometheus** as data sources.
- Build dashboards with metrics from Prometheus or logs from MySQL.

---

## Conclusion
By combining **Ansible**, **Prometheus**, **Node Exporter**, **Alertmanager**, **Grafana**, **Python**, and **MySQL**, you get a robust, automated monitoring solution. This approach ensures real-time insights, prompt alerts, and a central place to store and query logs – ultimately making infrastructure management smoother and more reliable.
