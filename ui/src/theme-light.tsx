import { ThemeConfig } from 'antd';
import styles from './styles.json';
const theme: ThemeConfig = {
    token: {
        wireframe: false,
        colorTextTertiary: styles.Colors.light['Text/colorTextTertiary'],
        colorTextQuaternary: styles.Colors.light['Text/colorTextQuaternary'],
        colorPrimaryBg: styles.Colors.light['Primary/colorPrimaryBg'],
        colorPrimaryBgHover: styles.Colors.light['Primary/colorPrimaryBgHover'],
        colorPrimaryBorder: styles.Colors.light['Primary/colorPrimaryBorder'],
        colorPrimaryBorderHover: styles.Colors.light['Primary/colorPrimaryBorderHover'],
        colorPrimaryHover: styles.Colors.light['Primary/colorPrimaryHover'],
        colorPrimary: styles.Colors.light['Primary/colorPrimary'],
        colorInfo: styles.Colors.light['Primary/colorPrimary'],
        colorPrimaryActive: styles.Colors.light['Primary/colorPrimaryActive'],
        colorPrimaryTextHover: styles.Colors.light['Primary/colorPrimaryTextHover'],
        colorPrimaryText: styles.Colors.light['Primary/colorPrimaryText'],
        colorPrimaryTextActive: styles.Colors.light['Primary/colorPrimaryTextActive'],
        colorSuccessBg: styles.Colors.light['Success/colorSuccessBg'],
        colorSuccessBgHover: styles.Colors.light['Success/colorSuccessBgHover'],
        colorSuccessBorder: styles.Colors.light['Success/colorSuccessBorder'],
        colorSuccessBorderHover: styles.Colors.light['Success/colorSuccessBorderHover'],
        colorSuccessHover: styles.Colors.light['Success/colorSuccessHover'],
        colorSuccessActive: styles.Colors.light['Success/colorSuccessActive'],
        colorSuccessTextHover: styles.Colors.light['Success/colorSuccessTextHover'],
        colorSuccessTextActive: styles.Colors.light['Success/colorSuccessTextActive'],
        colorSuccessText: styles.Colors.light['Success/colorSuccessText'],
        colorSuccess: styles.Colors.light['Success/colorSuccess'],
        colorWarningBg: styles.Colors.light['Warning/colorWarningBg'],
        colorWarningBgHover: styles.Colors.light['Warning/colorWarningBgHover'],
        colorWarningBorder: styles.Colors.light['Warning/colorWarningBorder'],
        colorWarningBorderHover: styles.Colors.light['Warning/colorWarningBorderHover'],
        colorWarningHover: styles.Colors.light['Warning/colorWarningHover'],
        colorWarning: styles.Colors.light['Warning/colorWarning'],
        colorWarningActive: styles.Colors.light['Warning/colorWarningActive'],
        colorWarningTextHover: styles.Colors.light['Warning/colorWarningTextHover'],
        colorWarningText: styles.Colors.light['Warning/colorWarningText'],
        colorWarningTextActive: styles.Colors.light['Warning/colorWarningTextActive'],
        colorErrorBg: styles.Colors.light['Error/colorErrorBg'],
        colorErrorBgHover: styles.Colors.light['Error/colorErrorBgHover'],
        colorErrorBorder: styles.Colors.light['Error/colorErrorBorder'],
        colorErrorBorderHover: styles.Colors.light['Error/colorErrorBorderHover'],
        colorErrorHover: styles.Colors.light['Error/colorErrorHover'],
        colorError: styles.Colors.light['Error/colorError'],
        colorErrorActive: styles.Colors.light['Error/colorErrorActive'],
        colorErrorTextHover: styles.Colors.light['Error/colorErrorTextHover'],
        colorErrorText: styles.Colors.light['Error/colorErrorText'],
        colorErrorTextActive: styles.Colors.light['Error/colorErrorTextActive'],
        colorLinkHover: styles.Colors.light['colorLinkHover'],
        colorLinkActive: styles.Colors.light['colorLinkActive'],
        colorTextBase: styles.Colors.light['Text/colorTextBase'],
        colorTextSecondary: styles.Colors.light['Text/colorTextSecondary'],
        colorBgMask: styles.Colors.light['Background/colorBgMask']
    },
    components: {
        Button: {
            paddingInline: styles.global['Space/Padding/padding'],
            paddingInlineLG: styles.global['Space/Padding/padding'],
            paddingBlockSM: styles.global['Space/Padding/paddingXS']
        },
        Collapse: {
            colorBorder: styles.Colors.light['Border/colorBorderSecondary'],
            contentPadding: `${styles.global['Space/Padding/padding']}px ${styles.global['Space/Padding/paddingLG']}px`,
            headerPadding: `${styles.global['Space/Padding/padding']}px ${styles.global['Space/Padding/paddingLG']}px`
        },
        Layout: {
            bodyBg: styles.Colors.light['Fill/colorFillQuaternary'] !== undefined 
                ? styles.Colors.light['Fill/colorFillQuaternary'] 
                : '#fafbfa',
            headerBg: styles.Colors.light['Background/colorBgContainer'],
            headerPadding: `${styles.global['Size/sizeMD']}px 24px`,
            siderBg: styles.Colors.light['Text/colorTextBase']
        },
        Menu: {
            colorText: styles.Colors.light['Text/colorTextLight'],
            iconSize: 16,
            itemBg: styles.Colors.light['Text/colorTextBase'],
            itemActiveBg: styles.Colors.dark['Background/colorBgTextActive'],
            itemHoverBg: styles.Colors.dark['Background/colorBgTextHover'],
            itemMarginBlock: styles.global['BorderRadius/borderRadius'],
            itemMarginInline: styles.global['Space/Margin/margin'],
            itemSelectedColor: styles.Colors.light['Text/colorTextLight'],
            itemSelectedBg: styles.Colors.light['Primary/colorPrimaryActive']
        },
        Typography: {
            colorError: styles.Colors.light['Error/colorError'],
            colorErrorHover: styles.Colors.light['Error/colorError'],
            colorErrorActive: styles.Colors.light['Error/colorError'],
            colorLink: styles.Colors.light['colorLink'],
            colorLinkActive: styles.Colors.light['colorLinkActive'],
            colorLinkHover: styles.Colors.light['colorLinkHover'],
            colorSuccess: styles.Colors.light['Success/colorSuccess'],
            colorText: styles.Colors.light['Text/colorText'],
            colorTextDescription: styles.Colors.light['Text/colorTextDescription'],
            colorTextDisabled: styles.Colors.light['Text/colorTextDisabled'],
            colorTextHeading: styles.Colors.light['Text/colorTextHeading'],
            colorWarning: styles.Colors.light['Warning/colorWarning'],
            fontFamily: styles.global.Typography['Desktop/Normal'].fontFamily,
            fontSize: styles.global.Typography['Desktop/Normal'].fontSize,
            fontSizeHeading1: styles.global.Typography['Desktop/H1'].fontSize,
            fontSizeHeading2: styles.global.Typography['Desktop/H2'].fontSize,
            fontSizeHeading3: styles.global.Typography['Desktop/H3'].fontSize,
            fontSizeHeading4: styles.global.Typography['Desktop/H4'].fontSize,
            fontSizeHeading5: styles.global.Typography['Desktop/H5'].fontSize,
            lineHeight: styles.global.Typography['Desktop/Normal'].lineHeight,
            lineHeightHeading1: styles.global.Typography['Desktop/H1'].lineHeight,
            lineHeightHeading2: styles.global.Typography['Desktop/H2'].lineHeight,
            lineHeightHeading3: styles.global.Typography['Desktop/H3'].lineHeight,
            lineHeightHeading4: styles.global.Typography['Desktop/H4'].lineHeight,
            lineHeightHeading5: styles.global.Typography['Desktop/H5'].lineHeight,
            linkDecoration: 'underline',
            titleMarginBottom: 0,
            titleMarginTop: 0
        }
    }
};

export default theme;
