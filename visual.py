from PIL import Image, ImageDraw, ImageFont


def render_recap(your_name, chatter_name, your_messages_count, chatter_messages_count,
                 your_response_time, chatter_response_time, your_words, chatter_words):
    width, height = 1000, 900
    background_color = (40, 40, 40)
    text_color = (40, 40, 40)
    block_color = (255, 255, 255)
    accent_color = (255, 87, 34)

    img = Image.new("RGB", (width, height), background_color)
    draw = ImageDraw.Draw(img)

    try:
        font_title = ImageFont.truetype("Arial.ttf", 36)
        font_subtitle = ImageFont.truetype("Arial.ttf", 24)
        font_body = ImageFont.truetype("Arial.ttf", 18)
    except:
        print("no such font")
        font_title = ImageFont.load_default()
        font_subtitle = ImageFont.load_default()
        font_body = ImageFont.load_default()

    title = "Chat Recap"
    draw.text((width // 2 - draw.textlength(title, font=font_title) // 2, 20),
              title, font=font_title, fill=accent_color)

    draw.line([(50, 80), (950, 80)], fill=accent_color, width=3)

    blocks = [
        {"x": 50, "y": 100, "w": 440, "h": 250, "title": "Messages count", "content":
         f"{your_name}{' '*40}{chatter_name}\n  {your_messages_count}{' '*44}{chatter_messages_count}"},
        {"x": 510, "y": 100, "w": 440, "h": 250, "title": "Avg response time", "content":
         f"{your_name}: {your_response_time}s\n{chatter_name}: {chatter_response_time}s"},
        {"x": 50, "y": 400, "w": 900, "h": 400, "title": "Most used words", "content":
         your_name + ":\n" + "\n".join([f"{i+1}. {word}: {count}" for i, (word, count) in enumerate(your_words.items()) if i < 5])
         + "\n" + chatter_name + ":\n" + "\n".join([f"{i+1}. {word}: {count}" for i, (word, count) in enumerate(chatter_words.items()) if i < 5])},
    ]  # rework all that

    for block in blocks:
        spacing = 30
        block_x, block_y = block["x"], block["y"] + spacing
        block_w, block_h = block["w"], block["h"]

        draw.rounded_rectangle(
            (block_x, block_y, block_x + block_w, block_y + block_h),
            radius=20, fill=block_color
        )
        title_width = draw.textlength(block["title"], font=font_subtitle)
        title_x = block_x + (block_w - title_width) // 2
        draw.text(
            (title_x, block_y + 20),
            block["title"], font=font_subtitle, fill=accent_color
        )
        draw.text(
            (block_x + 40, block_y + 70),
            block["content"], font=font_body, fill=text_color
        )

    img.save("chat_recap.png")
    print(f"saved as chat_recap.png")
