#! -*- coding:utf-8 -*-



from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time
import json
import shutil

from PyPDF2 import PdfReader
# 定义要请求的多个URL列表
urls = ["https://istio.io/latest/zh/","https://istio.io/latest/zh/about/service-mesh","https://istio.io/latest/zh/about/solutions","https://istio.io/latest/zh/about/case-studies","https://istio.io/latest/zh/about/ecosystem","https://istio.io/latest/zh/about/deployment","https://istio.io/latest/zh/about/faq","https://istio.io/latest/zh/blog/","https://istio.io/latest/zh/news/","https://istio.io/latest/zh/get-involved/","https://istio.io/latest/zh/docs/","https://istio.io/latest/zh/docs/setup/getting-started","https://istio.io/latest/zh/docs/overview/","https://istio.io/latest/zh/docs/overview/what-is-istio/","https://istio.io/latest/zh/docs/overview/why-choose-istio/","https://istio.io/latest/zh/docs/overview/dataplane-modes/","https://istio.io/latest/zh/docs/concepts/","https://istio.io/latest/zh/docs/concepts/traffic-management/","https://istio.io/latest/zh/docs/concepts/security/","https://istio.io/latest/zh/docs/concepts/observability/","https://istio.io/latest/zh/docs/concepts/wasm/","https://istio.io/latest/zh/docs/setup/","https://istio.io/latest/zh/docs/setup/getting-started/","https://istio.io/latest/zh/docs/setup/platform-setup/","https://istio.io/latest/zh/docs/setup/platform-setup/alicloud/","https://istio.io/latest/zh/docs/setup/platform-setup/amazon-eks/","https://istio.io/latest/zh/docs/setup/platform-setup/azure/","https://istio.io/latest/zh/docs/setup/platform-setup/docker/","https://istio.io/latest/zh/docs/setup/platform-setup/gke/","https://istio.io/latest/zh/docs/setup/platform-setup/huaweicloud/","https://istio.io/latest/zh/docs/setup/platform-setup/ibm/","https://istio.io/latest/zh/docs/setup/platform-setup/k3d/","https://istio.io/latest/zh/docs/setup/platform-setup/kind/","https://istio.io/latest/zh/docs/setup/platform-setup/kops/","https://istio.io/latest/zh/docs/setup/platform-setup/gardener/","https://istio.io/latest/zh/docs/setup/platform-setup/kubesphere/","https://istio.io/latest/zh/docs/setup/platform-setup/microk8s/","https://istio.io/latest/zh/docs/setup/platform-setup/minikube/","https://istio.io/latest/zh/docs/setup/platform-setup/openshift/","https://istio.io/latest/zh/docs/setup/platform-setup/oci/","https://istio.io/latest/zh/docs/setup/platform-setup/tencent-cloud-mesh/","https://istio.io/latest/zh/docs/setup/install/","https://istio.io/latest/zh/docs/setup/install/istioctl/","https://istio.io/latest/zh/docs/setup/install/helm/","https://istio.io/latest/zh/docs/setup/install/multicluster/","https://istio.io/latest/zh/docs/setup/install/multicluster/before-you-begin/","https://istio.io/latest/zh/docs/setup/install/multicluster/multi-primary/","https://istio.io/latest/zh/docs/setup/install/multicluster/primary-remote/","https://istio.io/latest/zh/docs/setup/install/multicluster/multi-primary_multi-network/","https://istio.io/latest/zh/docs/setup/install/multicluster/primary-remote_multi-network/","https://istio.io/latest/zh/docs/setup/install/multicluster/verify/","https://istio.io/latest/zh/docs/setup/install/multiple-controlplanes/","https://istio.io/latest/zh/docs/setup/install/virtual-machine/","https://istio.io/latest/zh/docs/setup/install/external-controlplane/","https://istio.io/latest/zh/docs/setup/upgrade/","https://istio.io/latest/zh/docs/setup/upgrade/canary/","https://istio.io/latest/zh/docs/setup/upgrade/in-place/","https://istio.io/latest/zh/docs/setup/upgrade/helm/","https://istio.io/latest/zh/docs/setup/additional-setup/","https://istio.io/latest/zh/docs/setup/additional-setup/download-istio-release/","https://istio.io/latest/zh/docs/setup/additional-setup/config-profiles/","https://istio.io/latest/zh/docs/setup/additional-setup/compatibility-versions/","https://istio.io/latest/zh/docs/setup/additional-setup/gateway/","https://istio.io/latest/zh/docs/setup/additional-setup/sidecar-injection/","https://istio.io/latest/zh/docs/setup/additional-setup/customize-installation/","https://istio.io/latest/zh/docs/setup/additional-setup/customize-installation-helm/","https://istio.io/latest/zh/docs/setup/additional-setup/cni/","https://istio.io/latest/zh/docs/setup/additional-setup/pod-security-admission/","https://istio.io/latest/zh/docs/setup/additional-setup/dual-stack/","https://istio.io/latest/zh/docs/setup/additional-setup/getting-started-istio-apis/","https://istio.io/latest/zh/docs/ambient/","https://istio.io/latest/zh/docs/ambient/overview/","https://istio.io/latest/zh/docs/ambient/getting-started/","https://istio.io/latest/zh/docs/ambient/getting-started/deploy-sample-app/","https://istio.io/latest/zh/docs/ambient/getting-started/secure-and-visualize/","https://istio.io/latest/zh/docs/ambient/getting-started/enforce-auth-policies/","https://istio.io/latest/zh/docs/ambient/getting-started/manage-traffic/","https://istio.io/latest/zh/docs/ambient/getting-started/cleanup/","https://istio.io/latest/zh/docs/ambient/install/","https://istio.io/latest/zh/docs/ambient/install/platform-prerequisites/","https://istio.io/latest/zh/docs/ambient/install/helm/","https://istio.io/latest/zh/docs/ambient/install/istioctl/","https://istio.io/latest/zh/docs/ambient/upgrade/","https://istio.io/latest/zh/docs/ambient/upgrade/helm/","https://istio.io/latest/zh/docs/ambient/usage/","https://istio.io/latest/zh/docs/ambient/usage/add-workloads/","https://istio.io/latest/zh/docs/ambient/usage/verify-mtls-enabled/","https://istio.io/latest/zh/docs/ambient/usage/networkpolicy/","https://istio.io/latest/zh/docs/ambient/usage/l4-policy/","https://istio.io/latest/zh/docs/ambient/usage/waypoint/","https://istio.io/latest/zh/docs/ambient/usage/l7-features/","https://istio.io/latest/zh/docs/ambient/usage/extend-waypoint-wasm/","https://istio.io/latest/zh/docs/ambient/usage/troubleshoot-ztunnel/","https://istio.io/latest/zh/docs/ambient/usage/troubleshoot-waypoint/","https://istio.io/latest/zh/docs/ambient/architecture/","https://istio.io/latest/zh/docs/ambient/architecture/control-plane/","https://istio.io/latest/zh/docs/ambient/architecture/data-plane/","https://istio.io/latest/zh/docs/ambient/architecture/hbone/","https://istio.io/latest/zh/docs/ambient/architecture/traffic-redirection/","https://istio.io/latest/zh/docs/tasks/","https://istio.io/latest/zh/docs/tasks/traffic-management/","https://istio.io/latest/zh/docs/tasks/traffic-management/request-routing/","https://istio.io/latest/zh/docs/tasks/traffic-management/fault-injection/","https://istio.io/latest/zh/docs/tasks/traffic-management/traffic-shifting/","https://istio.io/latest/zh/docs/tasks/traffic-management/tcp-traffic-shifting/","https://istio.io/latest/zh/docs/tasks/traffic-management/request-timeouts/","https://istio.io/latest/zh/docs/tasks/traffic-management/circuit-breaking/","https://istio.io/latest/zh/docs/tasks/traffic-management/mirroring/","https://istio.io/latest/zh/docs/tasks/traffic-management/locality-load-balancing/","https://istio.io/latest/zh/docs/tasks/traffic-management/locality-load-balancing/before-you-begin/","https://istio.io/latest/zh/docs/tasks/traffic-management/locality-load-balancing/failover/","https://istio.io/latest/zh/docs/tasks/traffic-management/locality-load-balancing/distribute/","https://istio.io/latest/zh/docs/tasks/traffic-management/locality-load-balancing/cleanup/","https://istio.io/latest/zh/docs/tasks/traffic-management/ingress/","https://istio.io/latest/zh/docs/tasks/traffic-management/ingress/ingress-control/","https://istio.io/latest/zh/docs/tasks/traffic-management/ingress/secure-ingress/","https://istio.io/latest/zh/docs/tasks/traffic-management/ingress/ingress-sidecar-tls-termination/","https://istio.io/latest/zh/docs/tasks/traffic-management/ingress/ingress-sni-passthrough/","https://istio.io/latest/zh/docs/tasks/traffic-management/ingress/kubernetes-ingress/","https://istio.io/latest/zh/docs/tasks/traffic-management/ingress/gateway-api/","https://istio.io/latest/zh/docs/tasks/traffic-management/egress/","https://istio.io/latest/zh/docs/tasks/traffic-management/egress/egress-control/","https://istio.io/latest/zh/docs/tasks/traffic-management/egress/egress-tls-origination/","https://istio.io/latest/zh/docs/tasks/traffic-management/egress/egress-gateway/","https://istio.io/latest/zh/docs/tasks/traffic-management/egress/egress-gateway-tls-origination/","https://istio.io/latest/zh/docs/tasks/traffic-management/egress/wildcard-egress-hosts/","https://istio.io/latest/zh/docs/tasks/traffic-management/egress/egress-kubernetes-services/","https://istio.io/latest/zh/docs/tasks/traffic-management/egress/http-proxy/","https://istio.io/latest/zh/docs/tasks/security/","https://istio.io/latest/zh/docs/tasks/security/authentication/","https://istio.io/latest/zh/docs/tasks/security/authentication/jwt-route/","https://istio.io/latest/zh/docs/tasks/security/authentication/authn-policy/","https://istio.io/latest/zh/docs/tasks/security/authentication/claim-to-header/","https://istio.io/latest/zh/docs/tasks/security/authentication/mtls-migration/","https://istio.io/latest/zh/docs/tasks/security/cert-management/","https://istio.io/latest/zh/docs/tasks/security/cert-management/plugin-ca-cert/","https://istio.io/latest/zh/docs/tasks/security/cert-management/custom-ca-k8s/","https://istio.io/latest/zh/docs/tasks/security/authorization/","https://istio.io/latest/zh/docs/tasks/security/authorization/authz-http/","https://istio.io/latest/zh/docs/tasks/security/authorization/authz-tcp/","https://istio.io/latest/zh/docs/tasks/security/authorization/authz-jwt/","https://istio.io/latest/zh/docs/tasks/security/authorization/authz-custom/","https://istio.io/latest/zh/docs/tasks/security/authorization/authz-deny/","https://istio.io/latest/zh/docs/tasks/security/authorization/authz-ingress/","https://istio.io/latest/zh/docs/tasks/security/authorization/authz-td-migration/","https://istio.io/latest/zh/docs/tasks/security/authorization/authz-dry-run/","https://istio.io/latest/zh/docs/tasks/security/tls-configuration/","https://istio.io/latest/zh/docs/tasks/security/tls-configuration/workload-min-tls-version/","https://istio.io/latest/zh/docs/tasks/policy-enforcement/","https://istio.io/latest/zh/docs/tasks/policy-enforcement/rate-limit/","https://istio.io/latest/zh/docs/tasks/observability/","https://istio.io/latest/zh/docs/tasks/observability/telemetry/","https://istio.io/latest/zh/docs/tasks/observability/metrics/","https://istio.io/latest/zh/docs/tasks/observability/metrics/telemetry-api/","https://istio.io/latest/zh/docs/tasks/observability/metrics/tcp-metrics/","https://istio.io/latest/zh/docs/tasks/observability/metrics/customize-metrics/","https://istio.io/latest/zh/docs/tasks/observability/metrics/classify-metrics/","https://istio.io/latest/zh/docs/tasks/observability/metrics/querying-metrics/","https://istio.io/latest/zh/docs/tasks/observability/metrics/using-istio-dashboard/","https://istio.io/latest/zh/docs/tasks/observability/logs/","https://istio.io/latest/zh/docs/tasks/observability/logs/otel-provider/","https://istio.io/latest/zh/docs/tasks/observability/logs/access-log/","https://istio.io/latest/zh/docs/tasks/observability/logs/telemetry-api/","https://istio.io/latest/zh/docs/tasks/observability/distributed-tracing/","https://istio.io/latest/zh/docs/tasks/observability/distributed-tracing/overview/","https://istio.io/latest/zh/docs/tasks/observability/distributed-tracing/telemetry-api/","https://istio.io/latest/zh/docs/tasks/observability/distributed-tracing/skywalking/","https://istio.io/latest/zh/docs/tasks/observability/distributed-tracing/jaeger/","https://istio.io/latest/zh/docs/tasks/observability/distributed-tracing/opentelemetry/","https://istio.io/latest/zh/docs/tasks/observability/distributed-tracing/zipkin/","https://istio.io/latest/zh/docs/tasks/observability/distributed-tracing/sampling/","https://istio.io/latest/zh/docs/tasks/observability/distributed-tracing/lightstep/","https://istio.io/latest/zh/docs/tasks/observability/distributed-tracing/mesh-and-proxy-config/","https://istio.io/latest/zh/docs/tasks/observability/kiali/","https://istio.io/latest/zh/docs/tasks/observability/gateways/","https://istio.io/latest/zh/docs/tasks/extensibility/","https://istio.io/latest/zh/docs/tasks/extensibility/wasm-module-distribution/","https://istio.io/latest/zh/docs/examples/","https://istio.io/latest/zh/docs/examples/bookinfo/","https://istio.io/latest/zh/docs/examples/virtual-machines/","https://istio.io/latest/zh/docs/examples/microservices-istio/","https://istio.io/latest/zh/docs/examples/microservices-istio/prereq/","https://istio.io/latest/zh/docs/examples/microservices-istio/setup-kubernetes-cluster/","https://istio.io/latest/zh/docs/examples/microservices-istio/setup-local-computer/","https://istio.io/latest/zh/docs/examples/microservices-istio/single/","https://istio.io/latest/zh/docs/examples/microservices-istio/package-service/","https://istio.io/latest/zh/docs/examples/microservices-istio/bookinfo-kubernetes/","https://istio.io/latest/zh/docs/examples/microservices-istio/production-testing/","https://istio.io/latest/zh/docs/examples/microservices-istio/add-new-microservice-version/","https://istio.io/latest/zh/docs/examples/microservices-istio/add-istio/","https://istio.io/latest/zh/docs/examples/microservices-istio/enable-istio-all-microservices/","https://istio.io/latest/zh/docs/examples/microservices-istio/istio-ingress-gateway/","https://istio.io/latest/zh/docs/examples/microservices-istio/logs-istio/","https://istio.io/latest/zh/docs/ops/","https://istio.io/latest/zh/docs/ops/deployment/","https://istio.io/latest/zh/docs/ops/deployment/platform-requirements/","https://istio.io/latest/zh/docs/ops/deployment/security-model/","https://istio.io/latest/zh/docs/ops/deployment/architecture/","https://istio.io/latest/zh/docs/ops/deployment/deployment-models/","https://istio.io/latest/zh/docs/ops/deployment/vm-architecture/","https://istio.io/latest/zh/docs/ops/deployment/performance-and-scalability/","https://istio.io/latest/zh/docs/ops/deployment/application-requirements/","https://istio.io/latest/zh/docs/ops/configuration/","https://istio.io/latest/zh/docs/ops/configuration/mesh/","https://istio.io/latest/zh/docs/ops/configuration/mesh/webhook/","https://istio.io/latest/zh/docs/ops/configuration/mesh/app-health-check/","https://istio.io/latest/zh/docs/ops/configuration/mesh/configuration-scoping/","https://istio.io/latest/zh/docs/ops/configuration/traffic-management/","https://istio.io/latest/zh/docs/ops/configuration/traffic-management/protocol-selection/","https://istio.io/latest/zh/docs/ops/configuration/traffic-management/tls-configuration/","https://istio.io/latest/zh/docs/ops/configuration/traffic-management/traffic-routing/","https://istio.io/latest/zh/docs/ops/configuration/traffic-management/manage-mesh-certificates/","https://istio.io/latest/zh/docs/ops/configuration/traffic-management/dns/","https://istio.io/latest/zh/docs/ops/configuration/traffic-management/dns-proxy/","https://istio.io/latest/zh/docs/ops/configuration/traffic-management/network-topologies/","https://istio.io/latest/zh/docs/ops/configuration/traffic-management/multicluster/","https://istio.io/latest/zh/docs/ops/configuration/security/","https://istio.io/latest/zh/docs/ops/configuration/security/security-policy-examples/","https://istio.io/latest/zh/docs/ops/configuration/security/harden-docker-images/","https://istio.io/latest/zh/docs/ops/configuration/telemetry/","https://istio.io/latest/zh/docs/ops/configuration/telemetry/envoy-stats/","https://istio.io/latest/zh/docs/ops/configuration/telemetry/monitoring-multicluster-prometheus/","https://istio.io/latest/zh/docs/ops/configuration/extensibility/","https://istio.io/latest/zh/docs/ops/configuration/extensibility/wasm-pull-policy/","https://istio.io/latest/zh/docs/ops/best-practices/","https://istio.io/latest/zh/docs/ops/best-practices/deployment/","https://istio.io/latest/zh/docs/ops/best-practices/traffic-management/","https://istio.io/latest/zh/docs/ops/best-practices/security/","https://istio.io/latest/zh/docs/ops/best-practices/image-signing-validation/","https://istio.io/latest/zh/docs/ops/best-practices/observability/","https://istio.io/latest/zh/docs/ops/common-problems/","https://istio.io/latest/zh/docs/ops/common-problems/network-issues/","https://istio.io/latest/zh/docs/ops/common-problems/security-issues/","https://istio.io/latest/zh/docs/ops/common-problems/observability-issues/","https://istio.io/latest/zh/docs/ops/common-problems/injection/","https://istio.io/latest/zh/docs/ops/common-problems/validation/","https://istio.io/latest/zh/docs/ops/common-problems/upgrade-issues/","https://istio.io/latest/zh/docs/ops/diagnostic-tools/","https://istio.io/latest/zh/docs/ops/diagnostic-tools/istioctl/","https://istio.io/latest/zh/docs/ops/diagnostic-tools/proxy-cmd/","https://istio.io/latest/zh/docs/ops/diagnostic-tools/istioctl-describe/","https://istio.io/latest/zh/docs/ops/diagnostic-tools/istioctl-analyze/","https://istio.io/latest/zh/docs/ops/diagnostic-tools/check-inject/","https://istio.io/latest/zh/docs/ops/diagnostic-tools/controlz/","https://istio.io/latest/zh/docs/ops/diagnostic-tools/component-logging/","https://istio.io/latest/zh/docs/ops/diagnostic-tools/virtual-machines/","https://istio.io/latest/zh/docs/ops/diagnostic-tools/cni/","https://istio.io/latest/zh/docs/ops/diagnostic-tools/multicluster/","https://istio.io/latest/zh/docs/ops/integrations/","https://istio.io/latest/zh/docs/ops/integrations/certmanager/","https://istio.io/latest/zh/docs/ops/integrations/grafana/","https://istio.io/latest/zh/docs/ops/integrations/jaeger/","https://istio.io/latest/zh/docs/ops/integrations/kiali/","https://istio.io/latest/zh/docs/ops/integrations/prometheus/","https://istio.io/latest/zh/docs/ops/integrations/spire/","https://istio.io/latest/zh/docs/ops/integrations/zipkin/","https://istio.io/latest/zh/docs/ops/integrations/skywalking/","https://istio.io/latest/zh/docs/ops/integrations/loadbalancers/","https://istio.io/latest/zh/docs/releases/","https://istio.io/latest/zh/docs/releases/feature-stages/","https://istio.io/latest/zh/docs/releases/bugs/","https://istio.io/latest/zh/docs/releases/security-vulnerabilities/","https://istio.io/latest/zh/docs/releases/supported-releases/","https://istio.io/latest/zh/docs/releases/contribute/","https://istio.io/latest/zh/docs/releases/contribute/github/","https://istio.io/latest/zh/docs/releases/contribute/add-content/","https://istio.io/latest/zh/docs/releases/contribute/remove-content/","https://istio.io/latest/zh/docs/releases/contribute/build/","https://istio.io/latest/zh/docs/releases/contribute/front-matter/","https://istio.io/latest/zh/docs/releases/contribute/review/","https://istio.io/latest/zh/docs/releases/contribute/code-blocks/","https://istio.io/latest/zh/docs/releases/contribute/shortcodes/","https://istio.io/latest/zh/docs/releases/contribute/formatting/","https://istio.io/latest/zh/docs/releases/contribute/style-guide/","https://istio.io/latest/zh/docs/releases/contribute/terminology/","https://istio.io/latest/zh/docs/releases/contribute/diagrams/","https://istio.io/latest/zh/docs/releases/log/","https://istio.io/latest/zh/docs/reference/","https://istio.io/latest/zh/docs/reference/config/","https://istio.io/latest/zh/docs/reference/config/config-status/","https://istio.io/latest/zh/docs/reference/config/proxy_extensions/","https://istio.io/latest/zh/docs/reference/config/networking/","https://istio.io/latest/zh/docs/reference/config/security/","https://istio.io/latest/zh/docs/reference/config/security/conditions/","https://istio.io/latest/zh/docs/reference/config/security/normalization/","https://istio.io/latest/zh/docs/reference/config/metrics/","https://istio.io/latest/zh/docs/reference/config/type/","https://istio.io/latest/zh/docs/reference/config/analysis/","https://istio.io/latest/zh/docs/reference/config/analysis/ist0136/","https://istio.io/latest/zh/docs/reference/config/analysis/message-format/","https://istio.io/latest/zh/docs/reference/config/analysis/ist0109/","https://istio.io/latest/zh/docs/reference/config/analysis/ist0110/","https://istio.io/latest/zh/docs/reference/config/analysis/ist0159/","https://istio.io/latest/zh/docs/reference/config/analysis/ist0116/","https://istio.io/latest/zh/docs/reference/config/analysis/ist0137/","https://istio.io/latest/zh/docs/reference/config/analysis/ist0002/","https://istio.io/latest/zh/docs/reference/config/analysis/ist0135/","https://istio.io/latest/zh/docs/reference/config/analysis/ist0153/","https://istio.io/latest/zh/docs/reference/config/analysis/ist0151/","https://istio.io/latest/zh/docs/reference/config/analysis/ist0155/","https://istio.io/latest/zh/docs/reference/config/analysis/ist0154/","https://istio.io/latest/zh/docs/reference/config/analysis/ist0152/","https://istio.io/latest/zh/docs/reference/config/analysis/ist0164/","https://istio.io/latest/zh/docs/reference/config/analysis/ist0150/","https://istio.io/latest/zh/docs/reference/config/analysis/ist0162/","https://istio.io/latest/zh/docs/reference/config/analysis/ist0167/","https://istio.io/latest/zh/docs/reference/config/analysis/ist0166/","https://istio.io/latest/zh/docs/reference/config/analysis/ist0001/","https://istio.io/latest/zh/docs/reference/config/analysis/ist0125/","https://istio.io/latest/zh/docs/reference/config/analysis/ist0144/","https://istio.io/latest/zh/docs/reference/config/analysis/ist0163/","https://istio.io/latest/zh/docs/reference/config/analysis/ist0161/","https://istio.io/latest/zh/docs/reference/config/analysis/ist0157/","https://istio.io/latest/zh/docs/reference/config/analysis/ist0143/","https://istio.io/latest/zh/docs/reference/config/analysis/ist0107/","https://istio.io/latest/zh/docs/reference/config/analysis/ist0111/","https://istio.io/latest/zh/docs/reference/config/analysis/ist0160/","https://istio.io/latest/zh/docs/reference/config/analysis/ist0123/","https://istio.io/latest/zh/docs/reference/config/analysis/ist0102/","https://istio.io/latest/zh/docs/reference/config/analysis/ist0127/","https://istio.io/latest/zh/docs/reference/config/analysis/ist0128/","https://istio.io/latest/zh/docs/reference/config/analysis/ist0129/","https://istio.io/latest/zh/docs/reference/config/analysis/ist0103/","https://istio.io/latest/zh/docs/reference/config/analysis/ist0158/","https://istio.io/latest/zh/docs/reference/config/analysis/ist0118/","https://istio.io/latest/zh/docs/reference/config/analysis/ist0101/","https://istio.io/latest/zh/docs/reference/config/analysis/ist0106/","https://istio.io/latest/zh/docs/reference/config/analysis/ist0134/","https://istio.io/latest/zh/docs/reference/config/analysis/ist0108/","https://istio.io/latest/zh/docs/reference/config/analysis/ist0112/","https://istio.io/latest/zh/docs/reference/config/analysis/ist0132/","https://istio.io/latest/zh/docs/reference/config/analysis/ist0131/","https://istio.io/latest/zh/docs/reference/config/analysis/ist0130/","https://istio.io/latest/zh/docs/reference/commands/","https://istio.io/latest/zh/docs/reference/commands/install-cni/","https://istio.io/latest/zh/docs/reference/commands/istioctl/","https://istio.io/latest/zh/docs/reference/commands/pilot-agent/","https://istio.io/latest/zh/docs/reference/commands/pilot-discovery/","https://istio.io/latest/zh/docs/reference/glossary/","https://istio.io/latest/zh/docs/","https://istio.io/latest/zh/docs/ops/","https://istio.io/latest/zh/docs/ops/best-practices/","https://istio.io/latest/zh/docs/ops/deployment/deployment-models/#namespace-tenancy","https://istio.io/latest/zh/docs/ops/best-practices/traffic-management/"]



def is_file_open(filepath):
    """检查文件是否被其他进程占用"""
    try:
        # 尝试以独占模式打开文件
        with open(filepath, 'a'):
            return False
    except IOError:
        return True




def sanitize_filename(filename):
    """替换文件名中的非法字符"""
    # 这里定义允许的字符，可以根据需要修改
    allowed_chars = "-_.() abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    return ''.join(c if c in allowed_chars else '_' for c in filename)


def include_str_rename_pdf(targetPath, target_str, new_file_name):
    rename_mapping = []  # 用于存储旧文件名和新文件名的映射

    for filename in os.listdir(targetPath):
        if filename.endswith('.pdf'):
            pdf_path = os.path.join(targetPath, filename)

            while is_file_open(pdf_path):
                print(f'File {filename} is currently in use. Waiting for it to be free...')
                time.sleep(1)  # 等待文件释放

            try:
                with open(pdf_path, 'rb') as file:
                    reader = PdfReader(file)
                    found = False

                    for page in reader.pages:
                        text = page.extract_text()
                        if text and target_str in text:
                            found = True
                            break

                    if found:
                        sanitized_new_name = sanitize_filename(new_file_name)
                        rename_mapping.append((filename, sanitized_new_name))

            except Exception as e:
                print(f'Error processing {filename}: {e}')

    bgk_file_path = os.path.join(targetPath, 'bgk.txt')
    with open(bgk_file_path, 'w', encoding='utf-8') as bgk_file:
        for old_name, new_name in rename_mapping:
            bgk_file.write(f'{old_name} -> {new_name}\n')

    finished_folder = os.path.join(targetPath, 'finished')
    os.makedirs(finished_folder, exist_ok=True)  # 创建 finished 文件夹（如果不存在）

    for old_name, new_name in rename_mapping:
        old_pdf_path = os.path.join(targetPath, old_name)
        new_pdf_path = os.path.join(targetPath, new_name)

        if os.path.exists(new_pdf_path):
            os.remove(new_pdf_path)

        # 尝试重命名并捕获可能的异常
        try:
            os.rename(old_pdf_path, new_pdf_path)
            print(f'Renamed {old_name} to {new_name}')
            # 将重命名后的文件移动到 finished 文件夹
            shutil.move(new_pdf_path, os.path.join(finished_folder, new_name))
            print(f'Moved {new_name} to finished folder.')
        except Exception as e:
            print(f'Failed to rename {old_name} to {new_name}: {e}')

    if os.path.exists(bgk_file_path):
        os.remove(bgk_file_path)
        print(f'Deleted {bgk_file_path}')



# Chrome浏览器配置
chrome_options = webdriver.ChromeOptions()
appState = {
    "recentDestinations": [
        {
            "id": "Save as PDF",
            "origin": "local",
            "account": ""
        }
    ],
    "selectedDestinationId": "Save as PDF",
    "version": 2,
    "pageSize": 'A4'
}
chrome_options.add_experimental_option("prefs", {
    "printing.print_preview_sticky_settings.appState": json.dumps(appState),
    "download.default_directory": os.path.expanduser('~/Downloads')
})
chrome_options.add_argument('--kiosk-printing')

# 启动Chrome浏览器
# driver_path = "./chromedriver.exe"
# service = Service(driver_path)
# driver = webdriver.Chrome(service=service, options=chrome_options)
driver = webdriver.Chrome(options=chrome_options)



# 打印并保存为PDF
for url in urls:
    driver.get(url)

    # 等待页面加载完成
    time.sleep(10)

    # PDF打印
    driver.execute_script('window.print();')

    # 等待一段时间确保页面保存完成
    time.sleep(10)
    # 这里直接识别原始文件名，然后按照urls的index值进行重命名
    # 后面合并时专门按照pdf文件的大小进行合并即可

    include_str_rename_pdf('C:\\Users\\user\\Downloads',"Istio",str(urls.index(url))+".pdf")
driver.quit()
# C:\\Users\\user\\Downloads



# 合并所有PDF文件为一个最大的PDF文件
# merger = PdfMerger()

# for pdf_file in sorted(pdf_files):
#     merger.append(pdf_file)
#
# output_file = "merged_output.pdf"
# merger.write(output_file)
# merger.close()
#
# # 删除临时生成的单独PDF文件
# for pdf_file in pdf_files:
#     os.remove(pdf_file)
