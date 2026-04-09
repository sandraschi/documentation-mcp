import React, { useState, useEffect } from 'react';
import { AlertCircle, CheckCircle, RefreshCw, Zap, HardDrive, Activity } from 'lucide-react';

interface DockerStatus {
  daemon_healthy: boolean;
  daemon_hanging: boolean;
  checks: {
    docker_installed: boolean;
    docker_version?: { version: string };
    recent_images?: { count: number; images: Array<{ name: string; size: string; created: string }> };
    recent_containers?: { count: number; containers: Array<{ name: string; status: string; ports: string; created: string }> };
    container_summary?: { running: number; stopped: number; total: number };
    disk_usage?: { usage: string[] };
    docker_config?: { memory_mb?: number; cpus?: number; swap_mb?: number };
  };
  issues: string[];
  recommendations: string[];
  timestamp: string;
}

export function DockerDesktop() {
  const [status, setStatus] = useState<DockerStatus | null>(null);
  const [loading, setLoading] = useState(false);
  const [autofix, setAutofix] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [activeTab, setActiveTab] = useState<'status' | 'images' | 'containers'>('status');

  const checkStatus = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await fetch('/api/mcp/tool', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          tool: 'docker_desktop_status',
          arguments: { autofix }
        })
      });
      const data = await response.json();
      setStatus(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to check status');
    } finally {
      setLoading(false);
    }
  };

  const recoverDaemon = async () => {
    setLoading(true);
    setError(null);
    try {
      await fetch('/api/mcp/tool', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          tool: 'docker_daemon_recover',
          arguments: {}
        })
      });
      await checkStatus();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Recovery failed');
    } finally {
      setLoading(false);
    }
  };

  const updateDocker = async () => {
    setLoading(true);
    setError(null);
    try {
      await fetch('/api/mcp/tool', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          tool: 'docker_desktop_update',
          arguments: { full_wipe: false }
        })
      });
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Update failed');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    checkStatus();
  }, []);

  if (!status) {
    return (
      <div className="p-6 bg-white rounded-lg shadow">
        <div className="animate-pulse">
          <div className="h-8 bg-gray-200 rounded w-1/4 mb-4"></div>
          <div className="h-4 bg-gray-200 rounded w-3/4"></div>
        </div>
      </div>
    );
  }

  const isHealthy = status.daemon_healthy && !status.daemon_hanging;

  return (
    <div className="space-y-6 p-6">
      {/* Header */}
      <div className="bg-gradient-to-r from-blue-50 to-blue-100 rounded-lg p-6 border border-blue-200">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            {isHealthy ? (
              <CheckCircle className="w-8 h-8 text-green-600" />
            ) : (
              <AlertCircle className="w-8 h-8 text-red-600" />
            )}
            <div>
              <h2 className="text-2xl font-bold text-gray-900">Docker Desktop</h2>
              <p className="text-sm text-gray-600">
                {isHealthy ? '✅ Daemon Healthy' : '⚠️  Daemon Issue Detected'}
              </p>
            </div>
          </div>
          <div className="text-xs text-gray-500">
            Last checked: {new Date(status.timestamp).toLocaleTimeString()}
          </div>
        </div>
      </div>

      {/* Error Banner */}
      {error && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-4 text-red-800">
          {error}
        </div>
      )}

      {/* Quick Actions */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <button
          onClick={checkStatus}
          disabled={loading}
          className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50"
        >
          <RefreshCw className="w-4 h-4" />
          {loading ? 'Checking...' : 'Check Status'}
        </button>
        <button
          onClick={recoverDaemon}
          disabled={loading || isHealthy}
          className="flex items-center gap-2 px-4 py-2 bg-orange-600 text-white rounded-lg hover:bg-orange-700 disabled:opacity-50"
        >
          <Zap className="w-4 h-4" />
          Recover Daemon
        </button>
        <button
          onClick={updateDocker}
          disabled={loading}
          className="flex items-center gap-2 px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 disabled:opacity-50"
        >
          <Activity className="w-4 h-4" />
          Check for Updates
        </button>
      </div>

      {/* Tabs */}
      <div className="border-b border-gray-200">
        <div className="flex gap-4">
          <button
            onClick={() => setActiveTab('status')}
            className={`px-4 py-2 font-medium ${activeTab === 'status' ? 'border-b-2 border-blue-600 text-blue-600' : 'text-gray-600'}`}
          >
            Status & Config
          </button>
          <button
            onClick={() => setActiveTab('images')}
            className={`px-4 py-2 font-medium ${activeTab === 'images' ? 'border-b-2 border-blue-600 text-blue-600' : 'text-gray-600'}`}
          >
            Recent Images ({status.checks.recent_images?.count || 0})
          </button>
          <button
            onClick={() => setActiveTab('containers')}
            className={`px-4 py-2 font-medium ${activeTab === 'containers' ? 'border-b-2 border-blue-600 text-blue-600' : 'text-gray-600'}`}
          >
            Containers ({status.checks.container_summary?.total || 0})
          </button>
        </div>
      </div>

      {/* Content */}
      <div className="bg-white rounded-lg shadow p-6">
        {activeTab === 'status' && (
          <div className="space-y-6">
            {/* Docker Version */}
            {status.checks.docker_version?.version && (
              <div>
                <h3 className="font-semibold text-gray-900 mb-2">Docker Version</h3>
                <p className="text-sm text-gray-600 font-mono">{status.checks.docker_version.version}</p>
              </div>
            )}

            {/* Configuration */}
            {status.checks.docker_config && (
              <div>
                <h3 className="font-semibold text-gray-900 mb-3">Docker Desktop Config</h3>
                <div className="grid grid-cols-3 gap-4">
                  <div className="bg-blue-50 p-3 rounded">
                    <p className="text-xs text-gray-600">Memory</p>
                    <p className="text-lg font-semibold text-gray-900">
                      {status.checks.docker_config.memory_mb ? `${Math.round(status.checks.docker_config.memory_mb / 1024)}GB` : 'N/A'}
                    </p>
                  </div>
                  <div className="bg-blue-50 p-3 rounded">
                    <p className="text-xs text-gray-600">CPUs</p>
                    <p className="text-lg font-semibold text-gray-900">{status.checks.docker_config.cpus || 'N/A'}</p>
                  </div>
                  <div className="bg-blue-50 p-3 rounded">
                    <p className="text-xs text-gray-600">Swap</p>
                    <p className="text-lg font-semibold text-gray-900">
                      {status.checks.docker_config.swap_mb ? `${Math.round(status.checks.docker_config.swap_mb / 1024)}GB` : 'N/A'}
                    </p>
                  </div>
                </div>
              </div>
            )}

            {/* Container Summary */}
            {status.checks.container_summary && (
              <div>
                <h3 className="font-semibold text-gray-900 mb-3">Container Summary</h3>
                <div className="grid grid-cols-3 gap-4">
                  <div className="bg-green-50 p-3 rounded">
                    <p className="text-xs text-gray-600">Running</p>
                    <p className="text-lg font-semibold text-green-600">{status.checks.container_summary.running}</p>
                  </div>
                  <div className="bg-yellow-50 p-3 rounded">
                    <p className="text-xs text-gray-600">Stopped</p>
                    <p className="text-lg font-semibold text-yellow-600">{status.checks.container_summary.stopped}</p>
                  </div>
                  <div className="bg-gray-50 p-3 rounded">
                    <p className="text-xs text-gray-600">Total</p>
                    <p className="text-lg font-semibold text-gray-900">{status.checks.container_summary.total}</p>
                  </div>
                </div>
              </div>
            )}

            {/* Disk Usage */}
            {status.checks.disk_usage?.usage && (
              <div>
                <h3 className="font-semibold text-gray-900 mb-2 flex items-center gap-2">
                  <HardDrive className="w-4 h-4" />
                  Disk Usage
                </h3>
                <div className="bg-gray-50 p-3 rounded font-mono text-xs space-y-1">
                  {status.checks.disk_usage.usage.map((line, i) => (
                    <div key={i} className="text-gray-700">{line}</div>
                  ))}
                </div>
              </div>
            )}

            {/* Issues */}
            {status.issues.length > 0 && (
              <div>
                <h3 className="font-semibold text-gray-900 mb-2 text-red-600">Issues Detected</h3>
                <ul className="space-y-2">
                  {status.issues.map((issue, i) => (
                    <li key={i} className="text-sm text-red-700 flex items-start gap-2">
                      <AlertCircle className="w-4 h-4 mt-0.5 flex-shrink-0" />
                      {issue}
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {/* Recommendations */}
            {status.recommendations.length > 0 && (
              <div>
                <h3 className="font-semibold text-gray-900 mb-2">Recommendations</h3>
                <ul className="space-y-2">
                  {status.recommendations.map((rec, i) => (
                    <li key={i} className="text-sm text-gray-700 flex items-start gap-2">
                      <CheckCircle className="w-4 h-4 mt-0.5 flex-shrink-0 text-blue-600" />
                      {rec}
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        )}

        {activeTab === 'images' && (
          <div>
            <h3 className="font-semibold text-gray-900 mb-4">Last 10 Built Images</h3>
            {status.checks.recent_images?.images && status.checks.recent_images.images.length > 0 ? (
              <div className="overflow-x-auto">
                <table className="w-full text-sm">
                  <thead className="bg-gray-50">
                    <tr>
                      <th className="px-4 py-2 text-left text-gray-700 font-semibold">Name</th>
                      <th className="px-4 py-2 text-left text-gray-700 font-semibold">Size</th>
                      <th className="px-4 py-2 text-left text-gray-700 font-semibold">Created</th>
                    </tr>
                  </thead>
                  <tbody>
                    {status.checks.recent_images.images.map((img, i) => (
                      <tr key={i} className="border-t border-gray-200 hover:bg-gray-50">
                        <td className="px-4 py-2 font-mono text-xs text-gray-900 truncate">{img.name}</td>
                        <td className="px-4 py-2 text-xs text-gray-600">{img.size}</td>
                        <td className="px-4 py-2 text-xs text-gray-600">{new Date(img.created).toLocaleString()}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            ) : (
              <p className="text-gray-500 text-sm">No images found</p>
            )}
          </div>
        )}

        {activeTab === 'containers' && (
          <div>
            <h3 className="font-semibold text-gray-900 mb-4">Last 10 Containers</h3>
            {status.checks.recent_containers?.containers && status.checks.recent_containers.containers.length > 0 ? (
              <div className="overflow-x-auto">
                <table className="w-full text-sm">
                  <thead className="bg-gray-50">
                    <tr>
                      <th className="px-4 py-2 text-left text-gray-700 font-semibold">Name</th>
                      <th className="px-4 py-2 text-left text-gray-700 font-semibold">Status</th>
                      <th className="px-4 py-2 text-left text-gray-700 font-semibold">Ports</th>
                      <th className="px-4 py-2 text-left text-gray-700 font-semibold">Created</th>
                    </tr>
                  </thead>
                  <tbody>
                    {status.checks.recent_containers.containers.map((cont, i) => (
                      <tr key={i} className="border-t border-gray-200 hover:bg-gray-50">
                        <td className="px-4 py-2 font-mono text-xs text-gray-900 truncate">{cont.name}</td>
                        <td className="px-4 py-2 text-xs">
                          <span className={`px-2 py-1 rounded text-white text-xs font-semibold ${
                            cont.status.includes('Up') ? 'bg-green-600' : 'bg-gray-600'
                          }`}>
                            {cont.status}
                          </span>
                        </td>
                        <td className="px-4 py-2 text-xs text-gray-600 truncate">{cont.ports || '-'}</td>
                        <td className="px-4 py-2 text-xs text-gray-600">{new Date(cont.created).toLocaleString()}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            ) : (
              <p className="text-gray-500 text-sm">No containers found</p>
            )}
          </div>
        )}
      </div>

      {/* Options */}
      <div className="bg-gray-50 rounded-lg p-4">
        <label className="flex items-center gap-2 text-sm text-gray-700">
          <input
            type="checkbox"
            checked={autofix}
            onChange={(e) => setAutofix(e.target.checked)}
            className="w-4 h-4"
          />
          <span>Auto-fix issues when checking status</span>
        </label>
        <p className="text-xs text-gray-500 mt-2 ml-6">
          If enabled, will automatically attempt to recover hanging daemon
        </p>
      </div>
    </div>
  );
}

export default DockerDesktop;
