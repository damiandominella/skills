# skills

Test

Collection of useful skills I want to own and manage.

## Linking skills to Cursor or Claude (symlink)

To use these skills from Cursor or Claude without copying files, symlink this repo (or individual skill folders) into the app’s skills directory.

### Cursor

Skills live under `~/.cursor/skills/`. From this repo’s parent directory:

```bash
# Link the whole repo so all skills are available
ln -s "$(pwd)/skills" ~/.cursor/skills/skills

# Or link one skill (e.g. breaking-changes)
ln -s "$(pwd)/skills/breaking-changes" ~/.cursor/skills/breaking-changes
```

Restart Cursor (or reload the window) so it picks up the links.

### Claude

If your Claude setup uses a custom skills/extensions directory, symlink the same way into that directory (path depends on your OS and Claude version—check Claude’s docs for the correct location).
