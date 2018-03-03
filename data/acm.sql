/*
Navicat SQLite Data Transfer

Source Server         : acm_problem
Source Server Version : 30714
Source Host           : :0

Target Server Type    : SQLite
Target Server Version : 30714
File Encoding         : 65001

Date: 2018-03-03 12:23:25
*/

PRAGMA foreign_keys = OFF;

-- ----------------------------
-- Table structure for sqlite_sequence
-- ----------------------------
DROP TABLE IF EXISTS "main"."sqlite_sequence";
CREATE TABLE sqlite_sequence(name,seq);

-- ----------------------------
-- Records of sqlite_sequence
-- ----------------------------
INSERT INTO "main"."sqlite_sequence" VALUES ('tb_problem_type', 1);

-- ----------------------------
-- Table structure for tb_problem
-- ----------------------------
DROP TABLE IF EXISTS "main"."tb_problem";
CREATE TABLE "tb_problem" (
"id"  INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
"type_id"  INTEGER NOT NULL,
"name"  TEXT(256) NOT NULL,
"content"  BLOB(1024) NOT NULL
);

-- ----------------------------
-- Records of tb_problem
-- ----------------------------

-- ----------------------------
-- Table structure for tb_problem_type
-- ----------------------------
DROP TABLE IF EXISTS "main"."tb_problem_type";
CREATE TABLE "tb_problem_type" (
"id"  INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
"name"  TEXT(128) NOT NULL,
"dscp"  TEXT(1024)
);
