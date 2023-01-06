BUILD_DIR=./dev-builds

for config in ./configs/*; do
    DEVICE=`basename $config`
    VERSION=latest_`date +%Y%m%d_%H%M%S`
    DEVICE_BUILD_DIR=$BUILD_DIR/$DEVICE/$VERSION

    echo Building $DEVICE into $DEVICE_BUILD_DIR ...

    # Delete and recreate if exists
    rm -rf $BUILD_DIR/$DEVICE
    mkdir -p $BUILD_DIR/$DEVICE

    # Touch version file
    echo $VERSION > $BUILD_DIR/$DEVICE/version

    # Copy all required file to the target device build dir
    mkdir -p $DEVICE_BUILD_DIR/paniq_prop && cp -R paniq_prop/* $DEVICE_BUILD_DIR/paniq_prop
    mkdir -p $DEVICE_BUILD_DIR/lib && cp -R lib/* $DEVICE_BUILD_DIR/lib
    cp main.py $DEVICE_BUILD_DIR
    cp $config/config.py $DEVICE_BUILD_DIR
    cp $config/network_config.py $DEVICE_BUILD_DIR
done
