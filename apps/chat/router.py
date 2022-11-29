# router.py
import datetime

from databases.core import Database
from fastapi.param_functions import Depends
from fastapi.routing import APIRouter
from fastapi.requests import Request
# Memo 스키마
from sqlalchemy import select, delete
from sqlalchemy.dialects.mysql import insert
from sqlalchemy.orm import Session

from apps.chat.models import CcCharChat, CcChar, CcCharChatForLearn, CcCharChatLog
from apps.chat.schema import ChatCreate
# Memo 모델
from apps.chat.model import ChatModel, db_engine
from apps.chat.schema import ChatCreate, CharChatCreate
from apps.common.kogpt import run_kogpt, run_gpt3
import json
import logging
import torch

chat_router = APIRouter()
cm = ChatModel()
logging.basicConfig(level=logging.INFO)


# 디비 쿼리를 위한 종속성 주입을 위한 함수
def get_db_conn(request: Request):
    return request.state.db_conn  # middleware 에서 삽입해준 db_conn


@chat_router.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@chat_router.get("/chat")
async def chat(
        db: Database = Depends(get_db_conn)
):
    # TODO : 채팅 데이터를 받아오게끔 수정해야함
    query = insert(CcCharChat).values(
        CHAT_ROOM_NO=1,
        CHAR_NO=2,
        CHAT_CONT="안녕!",
    )

    await db.execute(query)

    # db.

    # await db.execute(sensei_insert)
    #
    saori_result_query = select(CcChar).where(CcChar.CHAR_NO == 1)
    sensei_result_query = select(CcChar).where(CcChar.CHAR_NO == 2)
    messages_result_query = select(CcCharChat).filter(CcCharChat.CHAT_ROOM_NO == 1)
    saori_result = await db.fetch_one(saori_result_query)
    sensei_result = await db.fetch_one(sensei_result_query)
    messages_result = await db.fetch_all(messages_result_query)

    messages = []

    for message in messages_result:
        if message["CHAR_NO"] == saori_result["CHAR_NO"]:
            messages.append(saori_result["CHAR_NAME"] + ":" + message["CHAT_CONT"])
        if message["CHAR_NO"] == sensei_result["CHAR_NO"]:
            messages.append(sensei_result["CHAR_NAME"] + ":" + message["CHAT_CONT"])

    messages.append(saori_result.CHAR_NAME + ":")

    prompt = saori_result.CHAR_INFO

    for message in messages:
        if message != saori_result.CHAR_NAME + ":":
            prompt += message + "\n"
        else:
            prompt += message

    result = generate_text(prompt, 128)  # run_kogpt(prompt, 64)
    # result = json.loads(result)["result"]
    origin_result = result

    refined_result = result.split(prompt)[len(result.split(prompt)) - 1]
    refined_result = refined_result.split(saori_result.CHAR_NAME + ":")[0]
    refined_result = refined_result.split("\n")[0]

    query = insert(CcCharChat).values(
        CHAT_ROOM_NO=1,
        CHAR_NO=1,
        CHAT_CONT=refined_result,
    )

    await db.execute(query)

    return {
        "message": refined_result,
        "original": origin_result
    }


@chat_router.post("/chat/reset")
async def chat_reset_post(
        db: Database = Depends(get_db_conn)
):
    try:
        # 기초 데이터 받아옴
        fetch_run_base_query = select(
            CcCharChat
        )

        message_all_learn_data = await db.fetch_all(fetch_run_base_query)

        insert_list = []

        for message in message_all_learn_data:
            if message["IS_LEARN"] == "N":
                insert_list.append({
                    "CHAT_ROOM_NO": message["CHAT_ROOM_NO"],
                    "CHAR_NO": message["CHAR_NO"],
                    "CHAT_CONT": message["CHAT_CONT"],
                    "IS_LEARN": message["IS_LEARN"],
                    "UPD_DT": datetime.datetime.now(),
                    "REG_DT": message["REG_DT"],
                })

        query = insert(CcCharChatLog).values(insert_list)
        await db.execute(query)

        # 챗 데이터 비우기
        delete_query = delete(CcCharChat).where(CcCharChat.IS_LEARN == "N")
        await db.execute(delete_query)

        # 가비지 데이터 비우기
        gc_query = delete(CcCharChatLog).where(CcCharChatLog.CHAR_NO == 0)
        await db.execute(gc_query)

        return {
            "result": 0,
        }

    except Exception as e:
        print(e)
        return {"result": 1}


@chat_router.post("/chat/load_students")
async def chat_load_student_post(
        db: Database = Depends(get_db_conn)
):
    result_list = []

    try:

        query = select(CcChar).where(CcChar.CHAR_TYPE == "C")
        students = await db.fetch_all(query)

        for student in students:
            result_list.append({
                "name": student.STD_CODE_NAME,
                "full_name": student.STD_FULL_NAME,
                "inc_id": student.STD_INC_ID,
                "std_id": student.STD_ID,
                "token": student.STD_TOKEN,
                "role": student.STD_ROLE,
                "error_msg": student.STD_ERROR_MSG,
                "short_name": student.CHAR_NAME,
                "status": student.STD_STATUS
            })

        return result_list

    except Exception as e:
        print(e)
        return result_list


@chat_router.post("/chat/error_raise")
async def chat_error_raise_post(
        req: CharChatCreate,
        db: Database = Depends(get_db_conn)
):
    try:
        query = insert(CcCharChat).values(
            CHAT_ROOM_NO=req.chatRoomNo,
            CHAR_NO=req.charNo,
            CHAT_CONT=req.chatCont,
        )

        await db.execute(query)

        return {
            "result": 0,
        }

    except Exception as e:
        print(e)
        return {"result": 1}


@chat_router.post("/chat")
async def chat_post(
        req: CharChatCreate,
        db: Database = Depends(get_db_conn)
):
    # TODO : 채팅 데이터를 받아오게끔 수정해야함
    query = insert(CcCharChat).values(
        CHAT_ROOM_NO=req.chatRoomNo,
        CHAR_NO=2,
        CHAT_CONT=req.chatCont,
        REG_ID="admin",
        REG_DT=datetime.datetime.now(),
        UPD_DT=datetime.datetime.now(),
        UPD_ID="admin",
    )

    await db.execute(query)

    # db.

    # await db.execute(sensei_insert)
    #
    saori_result_query = select(CcChar).where(CcChar.CHAR_NO == req.charNo)
    sensei_result_query = select(CcChar).where(CcChar.CHAR_NO == 2)
    messages_result_query = select(CcCharChat).filter(CcCharChat.CHAT_ROOM_NO == req.chatRoomNo)

    saori_result = await db.fetch_one(saori_result_query)
    sensei_result = await db.fetch_one(sensei_result_query)
    messages_result = await db.fetch_all(messages_result_query)

    messages = []

    for message in messages_result:
        if message["CHAR_NO"] == saori_result["CHAR_NO"]:
            messages.append(saori_result["CHAR_NAME"] + ":" + message["CHAT_CONT"])
        if message["CHAR_NO"] == sensei_result["CHAR_NO"]:
            messages.append(sensei_result["CHAR_NAME"] + ":" + message["CHAT_CONT"])

    messages.append(saori_result.CHAR_NAME + ":")

    prompt = saori_result.CHAR_INFO + "\n"

    for message in messages:
        if message != saori_result.CHAR_NAME + ":":
            prompt += message + "\n"
        else:
            prompt += message

    post_time = datetime.datetime.now()

    print("current time : " + str(datetime.datetime.now()))
    elipsed_time = datetime.datetime.now() - post_time

    # 로컬
    # result = generate_text(prompt, 64)

    try:
        result = run_gpt3(prompt, 64)
        origin_result = result
        refined_result = result

    except Exception as e:
        # 카카오브레인 kogptd
        print(e)
        result = run_kogpt(prompt, 64)
        result = json.loads(result)["result"]

        origin_result = result

        try:
            # result = run_kogpt2(prompt)[0]['generated_text']
            # origin_result = result


            refined_result = result.split(prompt)[len(result.split(prompt)) - 1]

            if refined_result.__contains__(":"):

                if refined_result.startswith("정보:"):
                    refined_result = result.split("\n")[len(result.split("\n")) - 1]
                else:
                    refined_result = refined_result.split(saori_result.CHAR_NAME + ":")[1]

                refined_result = refined_result.split("\n")[0]

                if refined_result.startswith(saori_result.CHAR_NAME + ":") and len(
                        refined_result.split(saori_result.CHAR_NAME + ":")[
                            len(refined_result.split(saori_result.CHAR_NAME + ":")) - 1]) > 0:
                    refined_result = refined_result.split(saori_result.CHAR_NAME + ":")[
                        len(refined_result.split(saori_result.CHAR_NAME + ":")) - 1]
                elif refined_result.startswith(sensei_result.CHAR_NAME + ":") and len(
                        refined_result.split(sensei_result.CHAR_NAME + ":")[
                            len(refined_result.split(sensei_result.CHAR_NAME + ":")) - 1]) > 0:
                    refined_result = refined_result.split(sensei_result.CHAR_NAME + ":")[
                        len(refined_result.split(sensei_result.CHAR_NAME + ":")) - 1]
                elif refined_result.startswith(saori_result.CHAR_NAME + ":" + sensei_result.CHAR_NAME + ":"):
                    refined_result = "선생님"

                if len(origin_result.split(sensei_result["CHAR_NAME"] + ":" + req.chatCont)) >= 2:
                    if len(origin_result.split(sensei_result["CHAR_NAME"] + ":" + req.chatCont)[1].split(
                            saori_result["CHAR_NAME"] + ":")) >= 2:
                        if len(origin_result.split(sensei_result["CHAR_NAME"] + ":" + req.chatCont)[1].split(
                                saori_result["CHAR_NAME"] + ":")[1].split("\n")) >= 2:
                            refined_result = \
                            origin_result.split(sensei_result["CHAR_NAME"] + ":" + req.chatCont)[1].split(
                                saori_result["CHAR_NAME"] + ":")[1].split("\n")[0]

                if refined_result.__contains__("<|endoftext|>"):
                    refined_result = refined_result.split("<|endoftext|>")[0]

        except Exception as e:
            print(e)
            refined_result = saori_result.STD_ERROR_MSG

    # skt kogpt2

    query = insert(CcCharChat).values(
        CHAT_ROOM_NO=req.chatRoomNo,
        CHAR_NO=req.charNo,
        CHAT_CONT=refined_result,
        REG_ID="admin",
        REG_DT=datetime.datetime.now(),
        UPD_DT=datetime.datetime.now(),
        UPD_ID="admin",
    )
    print("elipased current time : " + str(datetime.datetime.now()))
    print("elipased time : " + str(elipsed_time))

    await db.execute(query)

    # print("origin_result = " + origin_result)
    # logging.info("origin_result = " + origin_result)

    return {
        "message": refined_result,
        "origin_message": origin_result,
    }
