FROM quay.io/pypa/manylinux1_x86_64
RUN curl https://sh.rustup.rs -sSf | sh -s -- --default-toolchain nightly -y
ENV PATH="/root/.cargo/bin:$PATH"
