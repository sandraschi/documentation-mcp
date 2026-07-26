#!/usr/bin/env python3
"""MCP Standards Manager CLI."""

import click
import sys
from pathlib import Path
from typing import Optional

from .core import StandardsManager
from .compliance import ComplianceChecker
from .documentation import DocumentationManager
from .repository import RepositoryManager


@click.group()
@click.version_option(version="1.0.0")
@click.option('--config', '-c', type=click.Path(exists=True),
              help='Path to config file')
@click.option('--verbose', '-v', is_flag=True, help='Enable verbose output')
@click.pass_context
def cli(ctx: click.Context, config: Optional[str], verbose: bool) -> None:
    """MCP Standards Manager - Automated MCP ecosystem standards management.

    This tool helps maintain compliance with MCP standards across all repositories,
    manage documentation, and coordinate version updates.
    """
    ctx.ensure_object(dict)
    ctx.obj['verbose'] = verbose
    ctx.obj['config'] = Path(config) if config else None

    # Initialize core components
    try:
        standards_manager = StandardsManager(config_path=ctx.obj['config'])
        ctx.obj['standards_manager'] = standards_manager
        ctx.obj['compliance_checker'] = ComplianceChecker(standards_manager)
        ctx.obj['documentation_manager'] = DocumentationManager(standards_manager)
        ctx.obj['repository_manager'] = RepositoryManager(standards_manager)
    except Exception as e:
        click.echo(f"❌ Failed to initialize: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.argument('repo_path', type=click.Path(exists=True))
@click.option('--fix', is_flag=True, help='Automatically fix violations')
@click.option('--report', type=click.Path(), help='Save report to file')
@click.pass_context
def check_repo(ctx: click.Context, repo_path: str, fix: bool, report: Optional[str]) -> None:
    """Check repository for standards compliance."""
    checker = ctx.obj['compliance_checker']

    try:
        click.echo(f"🔍 Checking repository: {repo_path}")

        results = checker.check_repository(Path(repo_path))

        if results.violations:
            click.echo(f"❌ Found {len(results.violations)} violations:")
            for violation in results.violations:
                click.echo(f"  - {violation.rule}: {violation.message}")

            if fix:
                click.echo("🔧 Applying automatic fixes...")
                fixed = checker.fix_violations(results)
                click.echo(f"✅ Fixed {fixed} violations")
        else:
            click.echo("✅ Repository is standards compliant!")

        if report:
            checker.save_report(results, Path(report))
            click.echo(f"📄 Report saved to: {report}")

    except Exception as e:
        click.echo(f"❌ Error checking repository: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.option('--repos', type=click.Path(), help='Path to repositories directory')
@click.option('--parallel', is_flag=True, help='Run checks in parallel')
@click.option('--report', type=click.Path(), help='Save aggregate report to file')
@click.pass_context
def check_all_repos(ctx: click.Context, repos: Optional[str],
                   parallel: bool, report: Optional[str]) -> None:
    """Check all repositories for standards compliance."""
    checker = ctx.obj['compliance_checker']
    repo_manager = ctx.obj['repository_manager']

    try:
        repos_path = Path(repos) if repos else Path.cwd()

        if not repos_path.exists():
            click.echo(f"❌ Repositories path does not exist: {repos_path}", err=True)
            sys.exit(1)

        click.echo(f"🔍 Checking all repositories in: {repos_path}")

        repositories = repo_manager.discover_repositories(repos_path)
        click.echo(f"📁 Found {len(repositories)} repositories")

        if parallel:
            results = checker.check_repositories_parallel(repositories)
        else:
            results = checker.check_repositories_sequential(repositories)

        total_violations = sum(len(result.violations) for result in results.values())

        click.echo(f"📊 Results: {len(results)} repositories checked")
        click.echo(f"⚠️  Total violations: {total_violations}")

        # Show summary
        for repo_path, result in results.items():
            status = "❌" if result.violations else "✅"
            click.echo(f"  {status} {repo_path.name}: {len(result.violations)} violations")

        if report:
            aggregate_report = checker.create_aggregate_report(results)
            checker.save_report(aggregate_report, Path(report))
            click.echo(f"📄 Aggregate report saved to: {report}")

    except Exception as e:
        click.echo(f"❌ Error checking repositories: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.argument('version')
@click.option('--repos', type=click.Path(), help='Path to repositories directory')
@click.option('--dry-run', is_flag=True, help='Show what would be updated without making changes')
@click.pass_context
def update_versions(ctx: click.Context, version: str, repos: Optional[str], dry_run: bool) -> None:
    """Update FastMCP versions across all repositories."""
    standards_manager = ctx.obj['standards_manager']
    repo_manager = ctx.obj['repository_manager']

    try:
        repos_path = Path(repos) if repos else Path.cwd()

        click.echo(f"🔄 Updating FastMCP to version {version}")
        if dry_run:
            click.echo("🔍 Dry run mode - no changes will be made")

        # Validate version
        if not standards_manager.validate_fastmcp_version(version):
            click.echo(f"❌ Invalid FastMCP version: {version}", err=True)
            sys.exit(1)

        repositories = repo_manager.discover_repositories(repos_path)
        updated = 0

        for repo in repositories:
            if repo_manager.update_fastmcp_version(repo, version, dry_run=dry_run):
                updated += 1
                if not dry_run:
                    click.echo(f"✅ Updated {repo.name}")
                else:
                    click.echo(f"📝 Would update {repo.name}")

        if dry_run:
            click.echo(f"📊 Would update {updated} repositories")
        else:
            click.echo(f"✅ Successfully updated {updated} repositories")

    except Exception as e:
        click.echo(f"❌ Error updating versions: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.argument('repo_name')
@click.option('--type', type=click.Choice(['mcp-server', 'webapp', 'documentation']),
              default='mcp-server', help='Type of repository to create')
@click.option('--template', type=click.Choice(['python', 'typescript', 'minimal']),
              default='python', help='Template to use')
@click.option('--path', type=click.Path(), help='Path where to create the repository')
@click.pass_context
def create_repo(ctx: click.Context, repo_name: str, type: str,
               template: str, path: Optional[str]) -> None:
    """Create a new repository with full standards compliance."""
    repo_manager = ctx.obj['repository_manager']
    documentation_manager = ctx.obj['documentation_manager']

    try:
        base_path = Path(path) if path else Path.cwd()
        repo_path = base_path / repo_name

        click.echo(f"🏗️  Creating {type} repository: {repo_name}")
        click.echo(f"📁 Location: {repo_path}")
        click.echo(f"🎨 Template: {template}")

        # Create repository structure
        repo_manager.create_repository(repo_path, type, template)

        # Generate documentation
        documentation_manager.generate_repository_docs(repo_path, type)

        # Initialize standards compliance
        ctx.obj['compliance_checker'].initialize_compliance(repo_path)

        click.echo("✅ Repository created successfully!")
        click.echo(f"📚 Documentation generated in {repo_path}/docs/")
        click.echo(f"🧪 Tests initialized in {repo_path}/tests/")
        click.echo(f"🔧 CI/CD configured in {repo_path}/.github/")

        click.echo(f"\n🚀 Next steps:")
        click.echo(f"  cd {repo_path}")
        click.echo(f"  git init && git add .")
        click.echo(f"  # Edit configuration files as needed")
        click.echo(f"  # Run 'standards check-repo --repo .' to verify compliance")

    except Exception as e:
        click.echo(f"❌ Error creating repository: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.argument('repo_path', type=click.Path(exists=True))
@click.option('--type', type=click.Choice(['readme', 'install', 'changelog', 'prd', 'api']),
              help='Type of documentation to generate')
@click.option('--force', is_flag=True, help='Overwrite existing files')
@click.pass_context
def generate_docs(ctx: click.Context, repo_path: str, type: Optional[str], force: bool) -> None:
    """Generate documentation for a repository."""
    documentation_manager = ctx.obj['documentation_manager']

    try:
        repo_path = Path(repo_path)

        if type:
            click.echo(f"📝 Generating {type} documentation for {repo_path.name}")
            documentation_manager.generate_documentation(repo_path, type, force=force)
        else:
            click.echo(f"📚 Generating all documentation for {repo_path.name}")
            documentation_manager.generate_repository_docs(repo_path, force=force)

        click.echo("✅ Documentation generated successfully!")

    except Exception as e:
        click.echo(f"❌ Error generating documentation: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.option('--repos', type=click.Path(), help='Path to repositories directory')
@click.option('--format', type=click.Choice(['text', 'json', 'html']),
              default='text', help='Report format')
@click.option('--output', type=click.Path(), help='Output file path')
@click.pass_context
def compliance_report(ctx: click.Context, repos: Optional[str],
                     format: str, output: Optional[str]) -> None:
    """Generate a compliance report for all repositories."""
    checker = ctx.obj['compliance_checker']
    repo_manager = ctx.obj['repository_manager']

    try:
        repos_path = Path(repos) if repos else Path.cwd()
        repositories = repo_manager.discover_repositories(repos_path)

        click.echo(f"📊 Generating compliance report for {len(repositories)} repositories")

        results = checker.check_repositories_parallel(repositories)
        report = checker.create_aggregate_report(results)

        if format == 'json':
            output_data = report.to_json()
        elif format == 'html':
            output_data = report.to_html()
        else:
            output_data = report.to_text()

        if output:
            Path(output).write_text(output_data)
            click.echo(f"📄 Report saved to: {output}")
        else:
            click.echo(output_data)

    except Exception as e:
        click.echo(f"❌ Error generating report: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.option('--repos', type=click.Path(), help='Path to repositories directory')
@click.option('--enable-monitoring', is_flag=True, help='Enable monitoring setup')
@click.option('--enable-cicd', is_flag=True, help='Enable CI/CD setup')
@click.pass_context
def repo_status(ctx: click.Context, repos: Optional[str],
               enable_monitoring: bool, enable_cicd: bool) -> None:
    """Show status of all repositories."""
    repo_manager = ctx.obj['repository_manager']

    try:
        repos_path = Path(repos) if repos else Path.cwd()
        repositories = repo_manager.discover_repositories(repos_path)

        click.echo(f"📁 Repository Status Report")
        click.echo(f"📍 Base Path: {repos_path}")
        click.echo(f"📊 Total Repositories: {len(repositories)}")
        click.echo("=" * 80)

        for repo in repositories:
            status = repo_manager.get_repository_status(repo)

            click.echo(f"📦 {repo.name}")
            click.echo(f"   📍 Path: {repo}")
            click.echo(f"   📋 Type: {status.get('type', 'unknown')}")
            click.echo(f"   ✅ Standards: {status.get('standards_version', 'unknown')}")
            click.echo(f"   🔧 FastMCP: {status.get('fastmcp_version', 'unknown')}")
            click.echo(f"   📚 Docs: {'✅' if status.get('has_docs') else '❌'}")
            click.echo(f"   🧪 Tests: {'✅' if status.get('has_tests') else '❌'}")
            click.echo(f"   🔄 CI/CD: {'✅' if status.get('has_cicd') else '❌'}")

            if enable_monitoring and not status.get('has_monitoring'):
                click.echo("   📊 Setting up monitoring..."                repo_manager.setup_monitoring(repo)

            if enable_cicd and not status.get('has_cicd'):
                click.echo("   🔧 Setting up CI/CD..."                repo_manager.setup_cicd(repo)

            click.echo()

    except Exception as e:
        click.echo(f"❌ Error getting repository status: {e}", err=True)
        sys.exit(1)


if __name__ == "__main__":
    cli()