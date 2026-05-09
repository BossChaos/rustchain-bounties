import * as vscode from 'vscode';
import * as https from 'https';
import * as http from 'http';

// Status bar items
let walletStatusItem: vscode.StatusBarItem;
let minerStatusItem: vscode.StatusBarItem;
let epochStatusItem: vscode.StatusBarItem;

// Tree view data provider
class BountyTreeDataProvider implements vscode.TreeDataProvider<BountyItem> {
    private bounties: BountyItem[] = [];
    private _onDidChangeTreeData = new vscode.EventEmitter<BountyItem | undefined>();
    readonly onDidChangeTreeData = this._onDidChangeTreeData.event;

    async refresh(): Promise<void> {
        await this.fetchBounties();
        this._onDidChangeTreeData.fire(undefined);
    }

    private async fetchBounties(): Promise<void> {
        try {
            const options = {
                hostname: 'api.github.com',
                path: '/repos/Scottcjn/rustchain-bounties/issues?state=open&labels=bounty',
                method: 'GET',
                headers: {
                    'User-Agent': 'RustChain-VSCode-Extension',
                    'Accept': 'application/vnd.github.v3+json'
                }
            };

            const data = await this.httpRequest(options);
            const issues = JSON.parse(data);
            this.bounties = issues.map((issue: any) => new BountyItem(
                issue.title,
                issue.number.toString(),
                issue.html_url,
                issue.body?.substring(0, 100) || '',
                issue.labels?.map((l: any) => l.name) || []
            ));
        } catch (error) {
            vscode.window.showErrorMessage(`Failed to fetch bounties: ${error}`);
        }
    }

    private httpRequest(options: any): Promise<string> {
        return new Promise((resolve, reject) => {
            const req = https.request(options, (res) => {
                let data = '';
                res.on('data', chunk => data += chunk);
                res.on('end', () => resolve(data));
            });
            req.on('error', reject);
            req.end();
        });
    }

    getTreeItem(element: BountyItem): vscode.TreeItem {
        const treeItem = new vscode.TreeItem(element.label, vscode.TreeItemCollapsibleState.None);
        treeItem.command = {
            command: 'rustchain.openBounty',
            title: 'Open Bounty',
            arguments: [element]
        };
        treeItem.iconPath = new vscode.ThemeIcon('$(gift)');
        return treeItem;
    }

    getChildren(): BountyItem[] {
        return this.bounties;
    }
}

class BountyItem extends vscode.TreeItem {
    constructor(
        public readonly label: string,
        public readonly bountyId: string,
        public readonly url: string,
        public readonly description: string,
        public readonly labels: string[]
    ) {
        super(label, vscode.TreeItemCollapsibleState.None);
        this.tooltip = `${this.bountyId}: ${this.description}`;
        this.contextValue = 'bounty';
    }
}

// API helper functions
async function apiRequest(path: string): Promise<any> {
    const config = vscode.workspace.getConfiguration('rustchain');
    const nodeUrl = config.get('nodeUrl', 'https://50.28.86.131');
    const baseUrl = nodeUrl.replace('https://', '').replace('http://', '');
    const isHttps = nodeUrl.startsWith('https');
    
    return new Promise((resolve, reject) => {
        const req = (isHttps ? https : http).request({
            hostname: baseUrl.split(':')[0],
            port: baseUrl.includes(':') ? parseInt(baseUrl.split(':')[1]) : (isHttps ? 443 : 80),
            path: path,
            method: 'GET',
            rejectUnauthorized: false
        }, (res) => {
            let data = '';
            res.on('data', chunk => data += chunk);
            res.on('end', () => {
                try { resolve(JSON.parse(data)); }
                catch { resolve(data); }
            });
        });
        req.on('error', reject);
        req.setTimeout(5000, () => { req.destroy(); reject(new Error('Request timeout')); });
        req.end();
    });
}

async function fetchWalletBalance(): Promise<number> {
    try {
        const config = vscode.workspace.getConfiguration('rustchain');
        const walletName = config.get('walletName', 'RTC6d1f27d28961279f1034d9561c2403697eb55602');
        const data = await apiRequest(`/wallet/balance?wallet_id=${walletName}`);
        return data.balance || 0;
    } catch {
        return 0;
    }
}

async function fetchMinerStatus(): Promise<boolean> {
    try {
        const data = await apiRequest('/api/miners');
        return data.active === true || data.status === 'active' || (Array.isArray(data) && data.length > 0);
    } catch {
        return false;
    }
}

async function fetchEpochInfo(): Promise<{ current: number; target: number }> {
    try {
        const data = await apiRequest('/epoch');
        return {
            current: data.epoch || data.current_epoch || 0,
            target: data.target_epoch || (data.epoch || 0) + 1
        };
    } catch {
        return { current: 0, target: 1 };
    }
}

function updateWalletStatus(balance: number): void {
    walletStatusItem.text = `$(wallet) RTC: ${balance.toFixed(2)}`;
    walletStatusItem.show();
}

function updateMinerStatus(active: boolean): void {
    if (active) {
        minerStatusItem.text = '$(debug-start) Mining';
        minerStatusItem.color = '#00ff00';
    } else {
        minerStatusItem.text = '$(debug-stop) Not Mining';
        minerStatusItem.color = '#ff0000';
    }
    minerStatusItem.show();
}

function updateEpochStatus(epoch: number, target: number): void {
    epochStatusItem.text = `$(clock) Epoch: ${epoch}/${target}`;
    epochStatusItem.show();
}

async function refreshAll(): Promise<void> {
    const [balance, minerActive, epochInfo] = await Promise.all([
        fetchWalletBalance(),
        fetchMinerStatus(),
        fetchEpochInfo()
    ]);
    
    updateWalletStatus(balance);
    updateMinerStatus(minerActive);
    updateEpochStatus(epochInfo.current, epochInfo.target);
}

export function activate(context: vscode.ExtensionContext): void {
    // Create status bar items
    walletStatusItem = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Left, 100);
    minerStatusItem = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Left, 99);
    epochStatusItem = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Left, 98);

    // Register tree view
    const bountyProvider = new BountyTreeDataProvider();
    vscode.window.registerTreeDataProvider('rustchain-bounties', bountyProvider);
    bountyProvider.refresh();

    // Commands
    vscode.commands.registerCommand('rustchain.refreshBounties', () => bountyProvider.refresh());
    vscode.commands.registerCommand('rustchain.claimBounty', (item: BountyItem) => {
        vscode.env.openExternal(vscode.Uri.parse(item.url));
    });
    vscode.commands.registerCommand('rustchain.openBounty', (item: BountyItem) => {
        vscode.env.openExternal(vscode.Uri.parse(item.url));
    });

    // Quick actions button
    const quickActions = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Right, 200);
    quickActions.text = '$(rocket) Quick Actions';
    quickActions.command = 'rustchain.showQuickActions';
    quickActions.show();
    context.subscriptions.push(quickActions);

    vscode.commands.registerCommand('rustchain.showQuickActions', async () => {
        const choice = await vscode.window.showQuickPick([
            'Refresh Status',
            'View Bounties',
            'Open Wallet',
            'Claim Bounty'
        ], { placeHolder: 'RustChain Quick Actions' });
        
        if (choice === 'Refresh Status') {
            await refreshAll();
            vscode.window.showInformationMessage('Status refreshed!');
        } else if (choice === 'View Bounties') {
            vscode.commands.executeCommand('workbench.view.extension.rustchain-sidebar');
        }
    });

    // Initial update and interval
    refreshAll();
    setInterval(refreshAll, 60000); // Update every minute

    context.subscriptions.push(walletStatusItem, minerStatusItem, epochStatusItem);
}

export function deactivate(): void {}
