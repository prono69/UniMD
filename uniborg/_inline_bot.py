#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) Shrimadhav U K
from math import ceil
import asyncio
import json
import random
import re
from telethon import events, errors, custom
from uniborg.util import admin_cmd, humanbytes


@borg.on(admin_cmd(  # pylint:disable=E0602
    pattern="ib (.[^ ]*) (.*)"
))
async def _(event):
    # https://stackoverflow.com/a/35524254/4723940
    if event.fwd_from:
        return
    bot_username = event.pattern_match.group(1)
    search_query = event.pattern_match.group(2)
    try:
        output_message = ""
        bot_results = await event.client.inline_query(  # pylint:disable=E0602
            bot_username,
            search_query
        )
        i = 0
        for result in bot_results:
            output_message += "{} {} `{}`\n\n".format(
                result.title,
                result.description,
                ".icb " + bot_username + " " + str(i + 1) + " " + search_query
            )
            i = i + 1
        await event.edit(output_message)
    except Exception as e:
        await event.edit("{} did not respond correctly, for **{}**!\n\
            `{}`".format(bot_username, search_query, str(e)))


@borg.on(admin_cmd(  # pylint:disable=E0602
    pattern="icb (.[^ ]*) (.[^ ]*) (.*)"
))
async def _(event):
    if event.fwd_from:
        return
    await event.delete()
    bot_username = event.pattern_match.group(1)
    i_plus_oneth_result = event.pattern_match.group(2)
    search_query = event.pattern_match.group(3)
    try:
        bot_results = await event.client.inline_query(  # pylint:disable=E0602
            bot_username,
            search_query
        )
        message = await bot_results[int(i_plus_oneth_result) - 1].click(event.chat_id, reply_to=event.reply_to_msg_id, hide_via=True)
    except Exception as e:
        await event.edit(str(e))


# pylint:disable=E0602
if Config.TG_BOT_USER_NAME_BF_HER is not None and tgbot is not None:
    @tgbot.on(events.InlineQuery)  # pylint:disable=E0602
    async def inline_handler(event):
        builder = event.builder
        result = None
        query = event.text
        if event.query.user_id == borg.uid and query.startswith("@UniBorg"):
            rev_text = query[::-1]
            buttons = paginate_help(0, borg._plugins, "helpme")
            result = builder.article(
                "© @UniBorg",
                text="{}\nCurrently Loaded Plugins: {}".format(
                    query, len(borg._plugins)),
                buttons=buttons,
                link_preview=False
            )
        elif query.startswith("ytdl"):
            # input format should be ytdl URL
            p = re.compile("ytdl (.*)")
            b = p.search(event.text)
            ytdl_url = "https://www.google.com/url?q=" + b.group(1).strip()
            if ytdl_url.startswith("http"):
                command_to_exec = [
                    "youtube-dl",
                    "--no-warnings",
                    "--youtube-skip-dash-manifest",
                    "-j",
                    ytdl_url
                ]
                logger.info(command_to_exec)
                process = await asyncio.create_subprocess_exec(
                    *command_to_exec,
                    # stdout must a pipe to be accessible as process.stdout
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE,
                )
                # Wait for the subprocess to finish
                stdout, stderr = await process.communicate()
                e_response = stderr.decode().strip()
                # logger.info(e_response)
                t_response = stdout.decode().strip()
                logger.info(command_to_exec)
                if e_response:
                    error_message = e_response.replace("please report this issue on https://yt-dl.org/bug . Make sure you are using the latest version; see  https://yt-dl.org/update  on how to update. Be sure to call youtube-dl with the --verbose flag and include its complete output.", "")
                    # throw error
                    result = builder.article(
                        "YTDL Errors © @UniBorg",
                        text=f"{error_message} Powered by @UniBorg",
                        link_preview=False
                    )
                elif t_response:
                    x_reponse = t_response
                    if "\n" in x_reponse:
                        x_reponse, _ = x_reponse.split("\n")
                    response_json = json.loads(x_reponse)
                    save_ytdl_json_path = Config.TMP_DOWNLOAD_DIRECTORY + \
                        "/" + "YouTubeDL" + ".json"
                    with open(save_ytdl_json_path, "w", encoding="utf8") as outfile:
                        json.dump(response_json, outfile, ensure_ascii=False)
                    # logger.info(response_json)
                    inline_keyboard = []
                    duration = None
                    if "duration" in response_json:
                        duration = response_json["duration"]
                    if "formats" in response_json:
                        for formats in response_json["formats"]:
                            format_id = formats.get("format_id")
                            format_string = formats.get("format_note")
                            if format_string is None:
                                format_string = formats.get("format")
                            format_ext = formats.get("ext")
                            approx_file_size = ""
                            if "filesize" in formats:
                                approx_file_size = humanbytes(formats["filesize"])
                            cb_string_video = "ytdl|{}|{}|{}".format(
                                "video", format_id, format_ext)
                            if format_string is not None:
                                ikeyboard = [
                                    custom.Button.inline(
                                        " " + format_ext  + " video [" + format_string +
                                        "] ( " +
                                        approx_file_size + " )",
                                        data=(cb_string_video)
                                    )
                                ]
                            else:
                                # special weird case :\
                                ikeyboard = [
                                    custom.Button.inline(
                                        " " + approx_file_size + " ",
                                        data=cb_string_video
                                    )
                                ]
                            inline_keyboard.append(ikeyboard)
                        if duration is not None:
                            cb_string_64 = "ytdl|{}|{}|{}".format("audio", "64k", "mp3")
                            cb_string_128 = "ytdl|{}|{}|{}".format("audio", "128k", "mp3")
                            cb_string = "ytdl|{}|{}|{}".format("audio", "320k", "mp3")
                            inline_keyboard.append([
                                custom.Button.inline(
                                    "MP3 " + "(" + "64 kbps" + ")", data=cb_string_64
                                ),
                                custom.Button.inline(
                                    "MP3 " + "(" + "128 kbps" + ")", data=cb_string_128
                                )
                            ])
                            inline_keyboard.append([
                                custom.Button.inline(
                                    "MP3 " + "(" + "320 kbps" + ")", data=cb_string
                                )
                            ])
                    else:
                        format_id = response_json["format_id"]
                        format_ext = response_json["ext"]
                        cb_string_video = "ytdl|{}|{}|{}".format(
                            "video", format_id, format_ext)
                        inline_keyboard.append([
                            custom.Button.inline(
                                "video",
                                data=cb_string_video
                            )
                        ])
                    result = builder.article(
                        "YouTube © @UniBorg",
                        text="{} powered by @UniBorg".format(ytdl_url.replace("https://www.google.com/url?q=", "")),
                        buttons=inline_keyboard,
                        link_preview=True
                    )
        elif query.startswith("tb_btn"):
            result = builder.article(
                "Button Parser © @UniBorg",
                text=f"Button Parser © @UniBorg",
                buttons=[custom.Button.url("Source Code", "https://da.gd/YQgR7")],
                link_preview=True
            )
        elif query.startswith("c_button"):
            BTN_URL_REGEX = re.compile(r"(\{([^\[]+?)\}\<button(url|text):(?:/{0,2})(.+?)(:same)?\>)")
            reply_message = query.replace("c_button ", "")
            markdown_note = reply_message
            prev = 0
            note_data = ""
            buttons = []
            for match in BTN_URL_REGEX.finditer(markdown_note):
                # Check if btnurl is escaped
                n_escapes = 0
                to_check = match.start(1) - 1
                while to_check > 0 and markdown_note[to_check] == "\\":
                    n_escapes += 1
                    to_check -= 1
        
                # if even, not escaped -> create button
                if n_escapes % 2 == 0:
                    # create a thruple with button label, url, and newline status
                    buttons.append((match.group(2), match.group(4), bool(match.group(5))))
                    note_data += markdown_note[prev:match.start(1)]
                    prev = match.end(1)
        
                # if odd, escaped -> move along
                else:
                    note_data += markdown_note[prev:to_check]
                    prev = match.start(1) - 1
            else:
                note_data += markdown_note[prev:]

            message_text = note_data.strip()
            tl_ib_buttons = build_keyboard(buttons, match.group(3))
        
            # logger.info(message_text)
            # logger.info(tl_ib_buttons)

            try:
                result = builder.article(
                    "Button Generated" if tl_ib_buttons else "Proccessing..." ,
                    text=message_text if tl_ib_buttons else "Error",
                    buttons=tl_ib_buttons if tl_ib_buttons else [custom.Button.inline("Error", data="txt_prod_Please Do Not Press Proccessing... Again")],
                    link_preview=True
                )
            except ButtonUrlInvalidError:
                pass
        else:
            result = builder.article(
                "© @UniBorg",
                text="""Hi there. I will introduce you to UniBorg
You can log-in as Bot or User and do many cool things with your Telegram account.

All instructions to run @UniBorg in your device has been explained in https://github.com/Somto811/UniBorg""",
                buttons=[
                    [custom.Button.url("Contact the Creator", "https://telegram.dog/loxxi"), custom.Button.url(
                        "Tutorial", "https://telegra.ph/Tutorial-07-26")],
                    [custom.Button.url(
                        "Source Code", "https://github.com/Somto811/UniBorg"), custom.Button.url("Best Prank Ever", "https://da.gd/OpvE3")],
                    [custom.Button.url(
                        "Deploy to Heroku", "http://github.com/Somto811/UniBorg"), custom.Button.url("Fork Boost", "https://telegra.ph/Fork-Boost-07-28"), custom.Button.url("Premium Dyno Cheat", "https://telegra.ph/Premium-Dyno-Cheat-07-28")]
                ],
                link_preview=False
            )
        await event.answer([result] if result else None)


    @tgbot.on(events.callbackquery.CallbackQuery(  # pylint:disable=E0602
        data=re.compile(b"helpme_next\((.+?)\)")
    ))
    async def on_plug_in_callback_query_handler(event):
        if event.query.user_id == borg.uid:  # pylint:disable=E0602
            current_page_number = int(
                event.data_match.group(1).decode("UTF-8"))
            buttons = paginate_help(
                current_page_number + 1, borg._plugins, "helpme")
            # https://t.me/TelethonChat/115200
            await event.edit(buttons=buttons)
        else:
            reply_pop_up_alert = "Please get your own @UniBorg, and don't edit my messages!"
            await event.answer(reply_pop_up_alert, cache_time=0, alert=True)


    @tgbot.on(events.callbackquery.CallbackQuery(  # pylint:disable=E0602
        data=re.compile(b"helpme_prev\((.+?)\)")
    ))
    async def on_plug_in_callback_query_handler(event):
        if event.query.user_id == borg.uid:  # pylint:disable=E0602
            current_page_number = int(
                event.data_match.group(1).decode("UTF-8"))
            buttons = paginate_help(
                current_page_number - 1,
                borg._plugins,  # pylint:disable=E0602
                "helpme"
            )
            # https://t.me/TelethonChat/115200
            await event.edit(buttons=buttons)
        else:
            reply_pop_up_alert = "Please get your own @UniBorg, and don't edit my messages!"
            await event.answer(reply_pop_up_alert, cache_time=0, alert=True)


    @tgbot.on(events.callbackquery.CallbackQuery(  # pylint:disable=E0602
        data=re.compile(b"txt_prod_(.*)")
    ))
    async def on_plug_in_callback_query_handler(event):
        reply_pop_up_alert = event.data_match.group(1).decode("UTF-8")
        await event.answer(reply_pop_up_alert, cache_time=0, alert=True)


    @tgbot.on(events.callbackquery.CallbackQuery(  # pylint:disable=E0602
        data=re.compile(b"ub_plugin_(.*)")
    ))
    async def on_plug_in_callback_query_handler(event):
        plugin_name = event.data_match.group(1).decode("UTF-8")
        help_string = None
        try:
            help_string = borg._plugins[plugin_name].__doc__[
                0:125]  # pylint:disable=E0602
        except:
            pass
        if help_string is None:
            reply_pop_up_alert = "No DOCSTRING has been setup for {} plugin".format(plugin_name)
        else:
            reply_pop_up_alert = help_string
        reply_pop_up_alert += "\n\n Use .unload {} to remove this plugin\n\
            © @UniBorg".format(plugin_name)
        await event.answer(reply_pop_up_alert, cache_time=0, alert=True)


def paginate_help(page_number, loaded_plugins, prefix):
    number_of_rows = Config.NO_OF_BUTTONS_DISPLAYED_IN_H_ME_CMD
    number_of_cols = 2
    multi = "😇🤠🤡😈👿👹👺💀☠👻👽👾🤖💩😺😸😹😻😼😽🙀😿😾🙈🙉🙊👦👧👨👩👴👵👶😊❤️😜😌😚😁😎👨‍💻🥶🤒👍🤝🙌🦋🦌🦚🦜🏆🚴‍♂✈️💯📣🇳🇬"
    helpable_plugins = []
    for p in loaded_plugins:
        if not p.startswith("_"):
            helpable_plugins.append(p)
    helpable_plugins = sorted(helpable_plugins)
    modules = [custom.Button.inline(
        "{} {} {}".format(random.choice(list(multi)), x, random.choice(list(multi))),
        data="ub_plugin_{}".format(x))
        for x in helpable_plugins]
    pairs = list(zip(modules[::number_of_cols], modules[1::number_of_cols]))
    if len(modules) % number_of_cols == 1:
        pairs.append((modules[-1],))
    max_num_pages = ceil(len(pairs) / number_of_rows)
    modulo_page = page_number % max_num_pages
    if len(pairs) > number_of_rows:
        pairs = pairs[modulo_page * number_of_rows:number_of_rows * (modulo_page + 1)] + \
            [
            (custom.Button.inline("⏮", data="{}_prev({})".format(prefix, modulo_page)),
             custom.Button.inline("⏭", data="{}_next({})".format(prefix, modulo_page)))
        ]
    return pairs

def build_keyboard(buttons, tipe):
    keyb = []
    for btn in buttons:
        if btn[2] and keyb and tipe == "url":
            keyb[-1].append(custom.Button.url(btn[0], btn[1]))
        elif tipe == "url":
            keyb.append([custom.Button.url(btn[0], btn[1])])
        if btn[2] and keyb and tipe == "text":
            keyb[-1].append(custom.Button.inline(btn[0], data="txt_prod_{}".format(btn[1])))
        elif tipe == "text":
            keyb.append([custom.Button.inline(btn[0], data="txt_prod_{}".format(btn[1]))])
    return keyb
