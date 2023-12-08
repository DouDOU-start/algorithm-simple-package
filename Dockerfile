ARG BASE_VERSION

FROM hanglok/algorithm-base:${BASE_VERSION}

COPY rootfs /
COPY algorithm /algorithm

WORKDIR /algorithm

ARG NEXUS_IP

RUN pip install --upgrade pip --trusted-host ${NEXUS_IP} -i http://${NEXUS_IP}:8081/repository/group-pypi/simple && \
    pip install --no-cache-dir -r requirements.txt --trusted-host ${NEXUS_IP} -i http://${NEXUS_IP}:8081/repository/group-pypi/simple && \
    pip install minio requests --trusted-host ${NEXUS_IP} -i http://${NEXUS_IP}:8081/repository/group-pypi/simple


# ENTRYPOINT ["python"]
# CMD ["agent.py"]

CMD ["python", "agent.py"]