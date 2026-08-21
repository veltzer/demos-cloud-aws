-- Ubuntu system level dependencies for this project

-- because of conflict with containerd which is needed by "docker.io" below.
-- the old deps.py chose this per ubuntu version (22.04 / 24.04) read from
-- /etc/os-release; lua cannot do that, and the value was the same on both.
PACKAGES_REMOVE = {
    "containerd.io",
}

PACKAGES = {
    -- for compiling .net
    "dotnet-sdk-8.0",
    -- spell check md files
    "aspell",
    -- lint .sh and .bash files
    "shellcheck",
    -- ruby stuff
    "ruby-bundler",
    "rbenv",
    -- for scratch exercises
    "bash-static",
    -- for docker
    "docker.io",
    -- the right package for docker compose
    "docker-compose-v2",
    -- "docker-doc",
    -- "docker-buildx",
    -- "docker-clean",
    -- "docker-registry",
}
