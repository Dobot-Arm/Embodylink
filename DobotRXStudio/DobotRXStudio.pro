QT       += core gui websockets concurrent network

greaterThan(QT_MAJOR_VERSION, 4): QT += widgets

CONFIG += c++11

TARGET = EmbodyLink

contains(QT_ARCH, i386) {
    TARGET_OUTPUT_DIR=x86_output
} else {
    TARGET_OUTPUT_DIR=x64_output
}
CONFIG(release, debug|release): DESTDIR = $$PWD/../$${TARGET_OUTPUT_DIR}/Release
else:CONFIG(debug, debug|release): DESTDIR = $$PWD/../$${TARGET_OUTPUT_DIR}/Debug

# You can make your code fail to compile if it uses deprecated APIs.
# In order to do so, uncomment the following line.
#DEFINES += QT_DISABLE_DEPRECATED_BEFORE=0x060000    # disables all the APIs deprecated before Qt 6.0.0

SOURCES += \
    Config/AppConfig.cpp \
    Config/Hdf5FileConfig.cpp \
    Config/LerobotFileConfig.cpp \
    Config/RobotRecordAnnotation.cpp \
    Config/RobotRecordList.cpp \
    Config/RobotTaskConfig.cpp \
    Config/RobotTaskList.cpp \
    Config/RobotTaskUploadItem.cpp \
    Config/RobotTeleopState.cpp \
    Config/UserConfig.cpp \
    Crypto/AES.cpp \
    DobotRobot.cpp \
    ErrorCode.cpp \
    FormAnnotationHandle.cpp \
    FormAnnotationStep.cpp \
    FormAtomConfig.cpp \
    FormDataAnnotation.cpp \
    FormDataCloud.cpp \
    FormDataCollect.cpp \
    FormDataExport.cpp \
    FormDataExportProcess.cpp \
    FormDataList.cpp \
    FormDataPreview.cpp \
    FormDataUpload.cpp \
    DeviceInfoWidget/IDeviceInfoWidget.cpp \
    DeviceInfoWidget/DeviceInfoWidgetAtomMax.cpp \
    DeviceInfoWidget/DeviceInfoWidgetAtomW.cpp \
    DeviceInfoWidget/DeviceInfoWidgetUnknown.cpp \
    FormDeviceInfo.cpp \
    FormLogin.cpp \
    FormModelDeployInfer.cpp \
    FormModelTraining.cpp \
    FormStep.cpp \
    FormViewImage.cpp \
    Global.cpp \
    GuardedProcess.cpp \
    HelperTool/OSSUtilTool.cpp \
    HelperTool/PKLFileParser.cpp \
    HelperTool/RobotFileFormater.cpp \
    HttpBean/AtomTrainEnum.cpp \
    HttpBean/AtomTrainEnumType.cpp \
    HttpBean/AuthEnterpriseAdminRegister.cpp \
    HttpBean/AuthLoginBean.cpp \
    HttpBean/AuthLogoutBean.cpp \
    HttpBean/AuthPasswordResetBean.cpp \
    HttpBean/AuthRegisterBean.cpp \
    HttpBean/ComputeListBean.cpp \
    HttpBean/ConfigurationListBean.cpp \
    HttpBean/DeleteTaskBean.cpp \
    HttpBean/HttpBaseBean.cpp \
    HttpBean/InvitationCodeBean.cpp \
    HttpBean/LoginEmailCodeBean.cpp \
    HttpBean/LoginPhoneCodeBean.cpp \
    HttpBean/ModelListBean.cpp \
    HttpBean/OssGeneratePathBean.cpp \
    HttpBean/SendEmailCodeBean.cpp \
    HttpBean/SendPhoneCodeBean.cpp \
    HttpBean/TaskCreateBean.cpp \
    HttpBean/TaskDetailBean.cpp \
    HttpBean/TaskListBean.cpp \
    HttpBean/TaskLogBean.cpp \
    HttpBean/TaskTrainLogBean.cpp \
    HttpBean/TrainingDataAvailableBean.cpp \
    HttpBean/TrainingDataCreateBean.cpp \
    HttpBean/UserCreditsBean.cpp \
    HttpClient.cpp \
    HttpDobotHandler.cpp \
    LoadingUI.cpp \
    Logger.cpp \
    ModeTrainWidget/FormModeTrainCreate.cpp \
    ModeTrainWidget/FormModeTrainDetail.cpp \
    ModeTrainWidget/FormModeTrainGraphic.cpp \
    ModeTrainWidget/FormModeTrainLog.cpp \
    ModeTrainWidget/FormModeTrainMode.cpp \
    ModeTrainWidget/FormModeTrainSelectData.cpp \
    ModeTrainWidget/FormModeTrainShow.cpp \
    MsgBox.cpp \
    SubclassUI/MyViewDelegate.cpp \
    RobotPlotInfo.cpp \
    SubclassUI/ClickableLabel.cpp \
    SubclassUI/MyComboBox.cpp \
    SubclassUI/ViewDelegate.cpp \
    SubclassUI/ViewHeaderDelegate.cpp \
    SubclassUI/TerminalWidget.cpp \
    SubclassUI/AboutDialog.cpp \
    TimelineWidget/TimelineSlider.cpp \
    TimelineWidget/TimelineTracker.cpp \
    WebSocketClient.cpp \
    main.cpp \
    MainWidget.cpp

HEADERS += \
    Config/AppConfig.h \
    Config/Hdf5FileConfig.h \
    Config/LerobotFileConfig.h \
    Config/RobotRecordAnnotation.h \
    Config/RobotRecordList.h \
    Config/RobotTaskConfig.h \
    Config/RobotTaskList.h \
    Config/RobotTaskUploadItem.h \
    Config/RobotTeleopState.h \
    Config/TaskEnum.h \
    Config/UserConfig.h \
    Crypto/AES.h \
    DobotRobot.h \
    ErrorCode.h \
    FormAnnotationHandle.h \
    FormAnnotationStep.h \
    FormAtomConfig.h \
    FormDataAnnotation.h \
    FormDataCloud.h \
    FormDataCollect.h \
    FormDataExport.h \
    FormDataExportProcess.h \
    FormDataList.h \
    FormDataPreview.h \
    FormDataUpload.h \
    DeviceInfoWidget/IDeviceInfoWidget.h \
    DeviceInfoWidget/DeviceInfoWidgetAtomMax.h \
    DeviceInfoWidget/DeviceInfoWidgetAtomW.h \
    DeviceInfoWidget/DeviceInfoWidgetUnknown.h \
    FormDeviceInfo.h \
    FormLogin.h \
    FormModelDeployInfer.h \
    FormModelTraining.h \
    FormStep.h \
    FormViewImage.h \
    Global.h \
    GuardedProcess.h \
    HelperTool/OSSUtilTool.h \
    HelperTool/PKLFileParser.h \
    HelperTool/RobotFileFormater.h \
    HttpBean/AtomTrainEnum.h \
    HttpBean/AuthEnterpriseAdminRegister.h \
    HttpBean/AuthLoginBean.h \
    HttpBean/AuthLogoutBean.h \
    HttpBean/AuthPasswordResetBean.h \
    HttpBean/AuthRegisterBean.h \
    HttpBean/ComputeListBean.h \
    HttpBean/ConfigurationListBean.h \
    HttpBean/DeleteTaskBean.h \
    HttpBean/HttpBaseBean.h \
    HttpBean/HttpBeanHeader.h \
    HttpBean/InvitationCodeBean.h \
    HttpBean/LoginEmailCodeBean.h \
    HttpBean/LoginPhoneCodeBean.h \
    HttpBean/ModelListBean.h \
    HttpBean/OssGeneratePathBean.h \
    HttpBean/SendEmailCodeBean.h \
    HttpBean/SendPhoneCodeBean.h \
    HttpBean/TaskCreateBean.h \
    HttpBean/TaskDetailBean.h \
    HttpBean/TaskListBean.h \
    HttpBean/TaskLogBean.h \
    HttpBean/TaskTrainLogBean.h \
    HttpBean/TrainingDataAvailableBean.h \
    HttpBean/TrainingDataCreateBean.h \
    HttpBean/UserCreditsBean.h \
    HttpClient.h \
    HttpDobotHandler.h \
    LoadingUI.h \
    Logger.h \
    MainWidget.h \
    ModeTrainWidget/FormModeTrainCreate.h \
    ModeTrainWidget/FormModeTrainDetail.h \
    ModeTrainWidget/FormModeTrainGraphic.h \
    ModeTrainWidget/FormModeTrainLog.h \
    ModeTrainWidget/FormModeTrainMode.h \
    ModeTrainWidget/FormModeTrainSelectData.h \
    ModeTrainWidget/FormModeTrainShow.h \
    MsgBox.h \
    SubclassUI/MyViewDelegate.h \
    RobotPlotInfo.h \
    SubclassUI/ClickableLabel.h \
    SubclassUI/MyComboBox.h \
    SubclassUI/ViewDelegate.h \
    SubclassUI/ViewHeaderDelegate.h \
    SubclassUI/TerminalWidget.h \
    SubclassUI/AboutDialog.h \
    TimelineWidget/TimelineSlider.h \
    TimelineWidget/TimelineTracker.h \
    WebSocketClient.h

FORMS += \
    FormAnnotationHandle.ui \
    FormAnnotationStep.ui \
    FormAtomConfig.ui \
    FormDataAnnotation.ui \
    FormDataCloud.ui \
    FormDataCollect.ui \
    FormDataExport.ui \
    FormDataExportProcess.ui \
    FormDataList.ui \
    FormDataPreview.ui \
    FormDataUpload.ui \
    DeviceInfoWidget/DeviceInfoWidgetAtomMax.ui \
    DeviceInfoWidget/DeviceInfoWidgetAtomW.ui \
    DeviceInfoWidget/DeviceInfoWidgetUnknown.ui \
    FormDeviceInfo.ui \
    FormLogin.ui \
    FormModelDeployInfer.ui \
    FormModelTraining.ui \
    FormStep.ui \
    FormViewImage.ui \
    LoadingUI.ui \
    MainWidget.ui \
    ModeTrainWidget/FormModeTrainCreate.ui \
    ModeTrainWidget/FormModeTrainDetail.ui \
    ModeTrainWidget/FormModeTrainGraphic.ui \
    ModeTrainWidget/FormModeTrainLog.ui \
    ModeTrainWidget/FormModeTrainMode.ui \
    ModeTrainWidget/FormModeTrainSelectData.ui \
    ModeTrainWidget/FormModeTrainShow.ui \
    SubclassUI/AboutDialog.ui

# Default rules for deployment.
qnx: target.path = /tmp/$${TARGET}/bin
else: unix:!android: target.path = /opt/$${TARGET}/bin
!isEmpty(target.path): INSTALLS += target

linux {
    QMAKE_LFLAGS += "-Wl,-rpath,\'\$$ORIGIN\':\'\$$ORIGIN/lib\',--enable-new-dtags"
    # 生成的程序，可以直接双击运行而不用在命令行上运行
    QMAKE_LFLAGS += -no-pie
}

TRANSLATIONS += \
    res/lang/zh_CN.ts \
    res/lang/en.ts

RESOURCES += \
    resource.qrc

RC_FILE = res/image/myapp.rc

include(QCustomPlot/QCustomPlot.pri)
