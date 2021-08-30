FROM public.ecr.aws/lambda/python:3.8

COPY app.py requirements.txt ./
COPY model-weights.hdf5 model-weights.hdf5
RUN yum install -y mesa-libGL
# RUN cp -v /usr/lib64/libGL.so.1 /mylayer/python/lib/python3.8/site-packages/opencv_python.libs/
# RUN cp -v /usr/lib64/libGL.so.1.7.0 /mylayer/python/lib/python3.8/site-packages/opencv_python.libs/
# RUN cp -v /usr/lib64/libgthread-2.0.so.0 /mylayer/python/lib/python3.8/site-packages/opencv_python.libs/
# RUN cp -v /usr/lib64/libgthread-2.0.so.0 /mylayer/python/lib/python3.8/site-packages/opencv_python.libs/
# RUN cp -v /usr/lib64/libglib-2.0.so.0 /mylayer/python/lib/python3.8/site-packages/opencv_python.libs/
# RUN cp -v /usr/lib64/libGLX.so.0 /mylayer/python/lib/python3.8/site-packages/opencv_python.libs/
# RUN cp -v /usr/lib64/libX11.so.6 /mylayer/python/lib/python3.8/site-packages/opencv_python.libs/
# RUN cp -v /usr/lib64/libXext.so.6 /mylayer/python/lib/python3.8/site-packages/opencv_python.libs/
# RUN cp -v /usr/lib64/libGLdispatch.so.0 /mylayer/python/lib/python3.8/site-packages/opencv_python.libs/
# RUN cp -v /usr/lib64/libGLESv1_CM.so.1.2.0 /mylayer/python/lib/python3.8/site-packages/opencv_python.libs/
# RUN cp -v /usr/lib64/libGLX_mesa.so.0.0.0 /mylayer/python/lib/python3.8/site-packages/opencv_python.libs/
# RUN cp -v /usr/lib64/libGLESv2.so.2.1.0 /mylayer/python/lib/python3.8/site-packages/opencv_python.libs/
# RUN cp -v /usr/lib64/libxcb.so.1 /mylayer/python/lib/python3.8/site-packages/opencv_python.libs/
# RUN cp -v /usr/lib64/libXau.so.6 /mylayer/python/lib/python3.8/site-packages/opencv_python.libs/
# RUN cp -v /usr/lib64/libXau.so.6 /mylayer/python/lib/python3.8/site-packages/opencv_python.libs/
# RUN cp -v /lib64/libGLdispatch.so.0.0.0 /mylayer/python/lib/python3.8/site-packages/opencv_python.libs/

RUN python3.8 -m pip install -r requirements.txt -t .

CMD ["app.lambda_handler"]
