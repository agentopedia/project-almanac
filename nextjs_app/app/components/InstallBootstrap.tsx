"use client";
import {useEffect} from "react";

export default function InstallBootstrap() {
    useEffect(() => {
          // @ts-expect-error testing something
          import("bootstrap/dist/js/bootstrap.bundle.js");
        }, []);

    return <></>;
}