from modules.ai import ImageDallE, ChatGPT
from modules.audio import AudioRecorder, AudioProcess, TextToSpeech
from modules.cmc import crypto_price
import modules.voices as vc
import os


def main_menu():
    menu_items = ["1. Voice Assistant", "2. New Chat", "3. Load Chat", "4. Generate Image", "5. ElevenLabs T-T-S",
                  "6. Live Crypto Price", "7. List of available GPT models", "8. Exit"]
    print(f"\n{menu_items[0]}\n{menu_items[1]}\n{menu_items[2]}\n{menu_items[3]}\n{menu_items[4]}\n{menu_items[5]}"
          f"\n{menu_items[6]}\n{menu_items[7]}")


def main():
    try:
        while True:
            main_menu()
            choice = int(input("\nChoose from menu: "))

            if choice == 1:
                assistant = ChatGPT()
                transcribe = AudioProcess()

                while True:
                    recorder = AudioRecorder()
                    recorder.record()
                    print(f"\nYou: {transcribe.transcribe(recorder.file_name)}")

                    if "stop" not in transcribe.response_text.lower():
                        print(f"Assistant: {assistant.ask(transcribe.response_text)}")
                        assistant.speak()
                        continue
                    else:
                        chat_name = input("\nSave chat as: ")
                        assistant.save_chat(chat_name)
                        assistant.clear_chat()
                        break

            elif choice == 2:
                ai_1 = ChatGPT()
                print("\nType 'r' to return to main menu.")
                while True:
                    chat_input = input("\nYou: ")
                    if chat_input != "r":
                        print(f"Assistant: {ai_1.ask(chat_input)}")
                        continue
                    else:
                        chat_name = input("\nSave chat as: ")
                        ai_1.save_chat(chat_name)
                        ai_1.clear_chat()
                        print(f"\nChat '{chat_name}' saved successfully!")
                        break

            elif choice == 3:
                chat_list = os.listdir("chats")
                print("\nList of available chats:\n")
                for x in chat_list:
                    print(x)

                ai_2 = ChatGPT()
                chat_name = input("\nEnter chat name (eg. travel, prog): ")
                ai_2.load_chat(chat_name)

                print("\nType 'r' to return to main menu.")

                while True:
                    chat_input = input("\nYou: ")
                    if chat_input != "r":
                        print(f"Assistant: {ai_2.ask(chat_input)}")
                        continue
                    else:
                        ai_2.save_chat(chat_name)
                        ai_2.clear_chat()
                        break

            elif choice == 4:
                dall_e = ImageDallE()
                while True:
                    img_prompt = input("\nEnter image description ('r' to return): ")
                    if img_prompt != "r":
                        print(dall_e.generate_image(img_prompt))
                        save = input("\nDo you want to save the image ? (y/n): ")
                        if save == "y":
                            image_name = input("\nEnter name for image: ")
                            dall_e.save_image(image_name)
                            continue
                        else:
                            continue
                    else:
                        break

            elif choice == 5:
                list_voices = input("\nGet list of voices ? (y/n): ")
                if list_voices == "y":
                    with open("data/voices.txt", "r") as f:
                        vc_list = f.read()
                        print(vc_list)
                        print("\nUse the voice IDs in the list when using custom voice!")
                else:
                    print("\nYou can still choose a voice from the preset list before generating the T-T-S file.")

                text_for_tts = input("\nEnter text to generate tts ('r' to return): ")

                if text_for_tts != "r":
                    print("\n1. Rachel\n2. Clyde\n3. Serena\n4. Nicole\n5. Custom")

                    voice = input("\nChoose voice: ")
                    if voice == "1":
                        voice = vc.Rachel
                    elif voice == "2":
                        voice = vc.Clyde
                    elif voice == "3":
                        voice = vc.Serena
                    elif voice == "4":
                        voice = vc.Nicole
                    elif voice == "5":
                        voice_code = input("\nInput voice id: ")
                        voice = voice_code
                    else:
                        print(f"No voice chosen! Default voice auto selected.")
                        voice = vc.Rachel

                    play_choice = input("Do you want to play the file ? (y/n): ")
                    if play_choice == "y":
                        tts = TextToSpeech(text_for_tts, voice)
                        print("\nWait for playback...")
                        tts.play()
                        continue
                    else:
                        continue
                else:
                    continue

            elif choice == 6:
                while True:
                    symbol = input("\nEnter crypto symbol ('r' to return): ")
                    if symbol != "r":
                        price = crypto_price(symbol)
                        print(price)
                        continue
                    else:
                        break

            elif choice == 7:
                models = ChatGPT().get_models()
                print(f"\nList of models:\n\n{models}")
                # for x in models:
                #     print(x)

            elif choice == 8:
                print("\nBye Bye!")
                break

            else:
                print("\nItem not available!")
                continue

    except ValueError:
        print("\nItem not available!")
        main()
    except KeyboardInterrupt:
        print("\n\nBye Bye!")


if __name__ == "__main__":
    main()
