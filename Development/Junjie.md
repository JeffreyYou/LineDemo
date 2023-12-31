## 1. Progress Log

**Developer Name**: [Junjie Lyu]

### [Dec 15. 2023]

- **Time Spent:** 7hours
- **Tasks Completed:**
  - Decode https encrypted LINE traffic with Chrome add-on version
  - Locate LINE chat history db at _/data/data/jp.naver.line.android/databases/naver_line/chat_history_
- **Issues Encountered:**
  - LINE uses ssl pinning on all client applications making it impossible to bypass certificate verification without reverse-engineering the application
  - LINE uses letter Sealing (basically ECDH_WITH_AES_256_CBC) to double encrypt end-to-end traffics, making it impossible to decode the message only with the shared public keys
  - _chat_history_ section only includes texts, for other types of messages it appears to be empty or □
- **Solutions and Workarounds:**
  - Using Chrome add-on LINE could bypass ssl pinning
  - Locating secret keys could theoretically help decoding the message after letter sealing
  - Chat history could be easily accessed in the db
- **Next Steps:**
  - Find where pictures are stored
  - Access the db on a rooted Android VM from host machine
- Additional Notes
  - Null
 
### [Dec 18. 2023]

- **Time Spent:** 7hours
- **Tasks Completed:**
  - Figure out how LINE stores its chat history: messages & emoji is stored in the content column in chat_history, stickers are referenced by STKID in paramenter column, picture overviews are stored in cache, original pictures and other files are not referenced if not downloaded manually hence content column left empty
  - Find a way to access the naver_line sqlite db file in the root folder from windows to rooted android physical device.
- **Issues Encountered:**
  - For unkown reasons, can not access root folder on Android VMs from PC
- **Solutions and Workarounds:**
  - Will try WSA + LAN server app
- **Next Steps:**
  - 2 pissible approaches:
  - Reverse engineering LINE.exe to bypass ssl pinning, lcoate device private keys and decrypt letter sealing messages and impersonate original LINE packages to reply
  - Or look up the chat_history using scripts, download and recognize pictures and files with OpenCV and reply by auto lookup and paste scripts
- Additional Notes
  - Null


### [Dec 19. 2023]
- **Time Spent:** 10hours
- **Tasks Completed:**
  - Successfully bypass ssl pinning with LSPosed [JustTrustMe](https://github.com/Fuzion24/JustTrustMe), which I though would be the least possible solution as it is too popular and too old
  - Pick up some basic knowledge of OpenCV, algorithms are basically the same as in TensorFlow and Keras, but more friendly
- **Issues Encountered:**
  - Way too much difficult to reverse engineer LINE.exe
  - Failed to disable ssl pinning with [apk-mitm](https://github.com/shroudedcode/apk-mitm), seems LINE has mechanisms to prevent modifying and repatching apk cource files
  - Failed to disable ssl pinning with LSPosed/XPosed modules including [SSLUnpinning](https://github.com/ac-pm/SSLUnpinning_Xposed) and [Inspeckage](https://github.com/ac-pm/Inspeckage), and no one is mantainning them any longer
- **Solutions and Workarounds:**
  - Will try WSA + LAN server app
- **Next Steps:**
  - Figure out a way to decrypt letter sealing
  - Find a way to send message and download pictures & other files
- Additional Notes
  - Null


## 2. Code Changes

### `#TODO`
