script_dir_abs=$(cd "$(dirname "$0")" && pwd)
rm -rf "${script_dir_abs}"/public
echo "Removed '${script_dir_abs}/public'"