if [ ! -f .devcontainer/.env ]; then
    cp .devcontainer/.env.dist .devcontainer/.env
fi

echo "Environment prepared. Please edit .devcontainer/.env as needed."

for hook in .devcontainer/scripts/hooks/*; do
    hook_name=$(basename "$hook")
    cp "$hook" ".git/hooks/$hook_name"
    chmod +x ".git/hooks/$hook_name"
    echo "Installed hook: $hook_name"
done

# echo "Enter the name of the ssh key (default: id_rsa - leave empty to skip):"
# read ssh_key_name

# if [ -n "$ssh_key_name" ]; then
#     cp .devcontainer/add-keys.sh.dist .devcontainer/add-keys.sh
#     chmod +x .devcontainer/add-keys.sh
#     sed -i "s/id_rsa/$ssh_key_name/g" .devcontainer/add-keys.sh
# fi