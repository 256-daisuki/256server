async def on_message(message):
    # 自分のメッセージを無効
    if message.author == bot.user:
        return

    if message.content.startswith('$shell'):
        if message.author.id == 891521181990129675:
            cmd = message.content[7:]
            initial_directory = "/home/discord"  # 初期ディレクトリを変更してください

            try:
                # コマンドを実行するために、シェル自体も起動
                result = subprocess.run(
                    ["/bin/bash", "-c", f"{cmd}"],
                    cwd=initial_directory,
                    stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                    text=True, timeout=10, shell=False
                )
                output = result.stdout.strip()

                result_message = f"discord@256server:{initial_directory}$ {cmd}\n{output}"
            except Exception as e:
                result_message = f"Error: {str(e)}"

            response = f'```{result_message}```'
            await message.channel.send(response)
        else:
            await message.channel.send('256大好き!しか実行できません')

    await bot.process_commands(message)