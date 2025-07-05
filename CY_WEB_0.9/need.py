import subprocess
import sys
from pathlib import Path


def generate_requirements(output_file="requirements.txt", exclude_system_packages=True):
    """
    生成包含精确版本信息的requirements.txt

    Args:
        output_file: 输出文件名
        exclude_system_packages: 是否排除系统级包
    """
    # 执行pip freeze获取所有依赖
    result = subprocess.run(
        [sys.executable, "-m", "pip", "freeze"],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        print(f"Error: {result.stderr}")
        return False

    # 依赖列表
    requirements = result.stdout.splitlines()

    # 排除常见的系统包（可选）
    if exclude_system_packages:
        system_packages = {
            "setuptools", "wheel", "pip", "pkg-resources",
            "python", "distribute", "easy-install"
        }
        requirements = [
            line for line in requirements
            if not any(pkg in line.split("==")[0].lower() for pkg in system_packages)
        ]

    # 写入文件
    with open(output_file, "w") as f:
        f.write("# Auto-generated requirements with exact versions\n")
        f.write("# Run: pip install -r requirements.txt\n\n")
        f.write("\n".join(requirements))

    print(f"✅ 已生成 {output_file}，包含 {len(requirements)} 个依赖")
    return True


if __name__ == "__main__":
    success = generate_requirements()
    if success:
        print("\n下一步建议：")
        print("1. 检查requirements.txt中是否有不需要的包")
        print("2. 为关键依赖添加版本范围约束（例如: django>=4.0,<5.0）")
        print("3. 在新环境中测试安装: pip install -r requirements.txt")