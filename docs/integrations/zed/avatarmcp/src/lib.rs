use zed_extension_api as zed;

struct AvatarMcpExtension;

impl AvatarMcpExtension {
    fn new() -> Self {
        Self
    }
}

impl zed::Extension for AvatarMcpExtension {
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
            args: vec!["AvatarMCP extension loaded".to_string()],
            env: Default::default(),
        })
    }
}

zed::register_extension!(AvatarMcpExtension);
