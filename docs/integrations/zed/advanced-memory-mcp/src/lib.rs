use zed_extension_api as zed;

struct AdvancedMemoryMcpExtension;

impl AdvancedMemoryMcpExtension {
    fn new() -> Self {
        Self
    }
}

impl zed::Extension for AdvancedMemoryMcpExtension {
    fn new() -> Self {
        Self::new()
    }

    fn context_server_command(
        &mut self,
        _id: &zed::ContextServerId,
        _project: &zed::Project,
    ) -> zed::Result<zed::Command> {
        // For now, return a generic command - this will need to be updated
        // based on the actual Zed extension API
        Ok(zed::Command {
            command: "echo".to_string(),
            args: vec!["Advanced Memory MCP extension loaded".to_string()],
            env: Default::default(),
        })
    }
}

zed::register_extension!(AdvancedMemoryMcpExtension);
